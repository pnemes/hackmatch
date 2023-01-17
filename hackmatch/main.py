# This file is part of HackMatch, see <https://github.com/MestreLion/hackmatch>
# Copyright (C) 2023 Rodrigo Silva (MestreLion) <linux@rodrigosilva.com>
# License: GPLv3 or later, at your choice. See <http://www.gnu.org/licenses/gpl>

"""
Exapunks HACK*MATCH Bot
"""

import argparse
import logging
import sys
import typing as t

from . import config as c
from . import logic
from . import util as u

log = logging.getLogger(__name__)


def parse_args(argv: t.Optional[t.List[str]] = None):
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog=c.COPYRIGHT,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-q', '--quiet',
                       dest='loglevel',
                       const=logging.WARNING,
                       default=logging.INFO,
                       action="store_const",
                       help="Suppress informative messages.")

    group.add_argument('-v', '--verbose',
                       dest='loglevel',
                       const=logging.DEBUG,
                       action="store_const",
                       help="Verbose mode, output extra info.")

    args = parser.parse_args(argv)
    args.debug = args.loglevel == logging.DEBUG
    return args


def main(argv: t.Optional[t.List[str]] = None):
    """Main CLI entry point"""
    try:
        args = parse_args(argv)
        logging.basicConfig(
            level=args.loglevel,
            datefmt="%Y-%m-%d %H:%M:%S",
            format='[%(asctime)s %(levelname)-6.6s] %(name)-15s: %(message)s'
        )
        log.debug(args)
        sys.exit(logic.bot())
    except u.HMError as err:
        log.error(err)
        sys.exit(1)
    except Exception as err:
        log.exception(err)
        sys.exit(1)
    except KeyboardInterrupt:
        log.info("Stopping...")
        import signal, os
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        os.kill(os.getpid(), signal.SIGINT)
