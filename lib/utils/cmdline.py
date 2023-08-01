#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
import sys

from ..core.defaults import defaults
from ..utils.colors import W, Y, bad, warn
from ..utils.settings import (BASIC_HELP, COPYRIGHT, NAME, VERSION,
                              CheckImports, logotype)

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

config = ConfigParser()

try:
    import argparse
    from argparse import SUPPRESS, ArgumentError, ArgumentParser

except ImportError as im:
    err = im.name
    CheckImports(err).downloadLib()

finally:
    def get_actions(instance):
        for attr in ("option_list", "_group_actions", "_actions"):
            if hasattr(instance, attr):
                return getattr(instance, attr)

    def get_groups(parser):
        return getattr(parser, "option_groups", None) or getattr(parser, "_action_groups")

    def get_all_options(parser):
        retVal = set()

        for option in get_actions(parser):
            if hasattr(option, "option_strings"):
                retVal.update(option.option_strings)
            else:
                retVal.update(option._long_opts)
                retVal.update(option._short_opts)

        for group in get_groups(parser):
            for option in get_actions(group):
                if hasattr(option, "option_strings"):
                    retVal.update(option.option_strings)
                else:
                    retVal.update(option._long_opts)
                    retVal.update(option._short_opts)

        return retVal


OBS_OPT = {
    "--dns-bruter": "Use '--bruter' Instead",
}

DEP_OPT = {
    "--subdomain": "functionality Being Done Automatically",
}


def checkOldOptions(args):
    for _ in args:
        _ = _.split('=')[0].strip()
        if _ in OBS_OPT:
            errMsg = bad + "Option '%s' Is Obsolete" % _
            if OBS_OPT[_]:
                errMsg += " (Hint: %s)" % OBS_OPT[_]
            raise logging.warn(errMsg)
        elif _ in DEP_OPT:
            warnMsg = "Option '%s' Is Deprecated" % _
            if DEP_OPT[_]:
                warnMsg += " (Hint: %s)" % DEP_OPT[_]
            logging.warn(warnMsg)


def parser_cmd(argv=None):
    logotype()
    def formatter(prog): return argparse.HelpFormatter(prog, max_help_position=100)
    parser = ArgumentParser(usage="python " + Y + sys.argv[0] + W + " -u example.com", formatter_class=formatter)
    try:
        parser.add_argument("--hh", "--help-hack", dest="advancedHelp", action="store_true",
                            help="Show Advanced Help Message And Exit")

        parser.add_argument("--version", action='version', version=NAME + VERSION + ' | ' + COPYRIGHT,
                            help="Show Program's Version Number And Exit")

        parser.add_argument("-v", dest="verbose", action="store_true",
                            help="Verbosity For Sublister: True/False (default: False)")

        # Target options
        target = parser.add_argument_group(
            "Target", "At Least One Of These Options Has To Be Provided To Define The Target(s)")

        target.add_argument("-u", "--url", metavar="target", dest="domain",
                            help="Target URL As First Argument (e.g. python GulagScanner.py example.com)")

        target.add_argument("--disable-sublister", dest="disableSub", action="store_true",
                            help="Disable Subdomain Listing For Testing")

        target.add_argument("--bruter", dest="brute", action="store_true",
                            help="Bruteforcing Target To Find Associated Domains")

        target.add_argument("--subbruter", dest="subbrute", action="store_true",
                            help="Bruteforcing Target's Subdomains Using Subbrute Module")

        # Request options
        request = parser.add_argument_group(
            "Request", "These Options Can Be Used To Specify How To Connect To The Target URL")

        request.add_argument("--user-agent", dest="uagent",
                             help="Set HTTP User-Agent Header Value")

        request.add_argument("--random-agent", dest="randomAgent", action="store_true",
                             help="Set Randomly Selected HTTP User-Agent Header Value")

        request.add_argument("--host", dest="host",
                             help="HTTP Host Header Value")

        request.add_argument("--headers", dest="headers",
                             help="Set Custom Headers (e.g. \"Origin: example.com, ETag: 123\")")

        request.add_argument("--ignore-redirects", dest="ignoreRedirects", action="store_false",
                             help="Ignore Redirection Attempts")

        request.add_argument("--threads", dest="threads", default=defaults.threads, type=int,
                             help="Max Number Of Concurrent HTTP(s) Requests (Default %d)" % defaults.threads)

        # Search options
        search = parser.add_argument_group("Search", "These Options Can Be Used To Perform Advanced Searches")

        search.add_argument("-sC", "--search-censys", dest="censys", nargs="?", const="data/APIs/api.conf", type=str,
                            help="Perform search Using Censys API")

        search.add_argument("-sSh", "--search-shodan", dest="shodan", nargs="?", const="data/APIs/api.conf", type=str,
                            help="Perform Search Using Shodan API")

        search.add_argument("-sSt", "--search-st", dest="securitytrails", nargs="?", const="data/APIs/api.conf",
                            type=str, help="Perform Search Using SecurityTrails API")

        # Output options
        output = parser.add_argument_group("Output", "These Options Can Be Used To Save The Subdomains Results")

        output.add_argument("-o", "--output", dest="outSub", action="store_true",
                            help="Save The Subdomains Into: \"data/output/subdomains-[domain].txt\"")

        output.add_argument("--oG", "--output-good", dest="outSubG", action="store_true",
                            help="Save [Good Response] Subdomains Into: \"data/output/good-subdomains-[domain].txt\"")

        output.add_argument("--oI", "--output-ip", dest="outSubIP", action="store_true",
                            help="Save Subdomains IP Into: \"data/output/good-subdomains-[domain].txt\"")

        advancedHelp = True
        argv = sys.argv[1:]
        checkOldOptions(argv)

        for i in range(len(argv)):
            if argv[i] in ("-h", "--help"):
                advancedHelp = False
                for group in get_groups(parser)[:]:
                    found = False
                    for option in get_actions(group):
                        if option.dest not in BASIC_HELP:
                            option.help = SUPPRESS
                        else:
                            found = True
                    if not found:
                        get_groups(parser).remove(group)

        try:
            (args, _) = parser.parse_known_args(argv) if hasattr(
                parser, "parse_known_args") else parser.parse_args(argv)
        except UnicodeEncodeError as ex:
            print("\n %s%s\n" % bad, ex)
            raise SystemExit
        except SystemExit:
            if "-h" in argv and not advancedHelp or "--help" in argv and not advancedHelp:
                print("\n" + warn + "To See Full List Of Options Run With '-hh' Or '--help-hack'\n")
            raise

        if not args.domain:
            errMsg = "Missing A Mandatory Option (-u, --url). Use -h For Basic And -hh For Advanced Help\n"
            parser.error(errMsg)

        return parser.parse_args(), parser.error
    except (ArgumentError, TypeError) as ex:
        parser.error(str(ex))
    debugMsg = "Parsing Command Line"
    logging.debug(debugMsg)
