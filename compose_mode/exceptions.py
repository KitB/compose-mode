#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ComposeModeException(Exception):
    """ Base exception for compose-mode """


class ComposeModeYmlNotFound(ComposeModeException):
    """ Exception raised when no configuration file was found """


def main():
    pass

if __name__ == '__main__':
    main()
