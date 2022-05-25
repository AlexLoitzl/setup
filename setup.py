#!/usr/bin/python

import argparse, subprocess

parser = argparse.ArgumentParser(description='Specify which task should be done')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--wacom', metavar='Screenname',
                    help='Map to given Screen e.g. eDP,DisplayPort-4, HDMI-A-0')
group.add_argument('--setup', action='store_true',
                    help='Setup process for new system')
group.add_argument('--wifi', action='store_true',
                    help='Setup wifi again(execute as sudo)')
group.add_argument('--audio', action='store_true',
                    help='Provide information about audio controls')
group.add_argument('--power', action='store_true',
                    help='Provide information about power information')
group.add_argument('--display', action='store_true', help='Provide information about configuring additional screens')

args = parser.parse_args()

if args.wacom:
    ret = subprocess.run('xsetwacom --list', shell=True, capture_output=True)
    # Get id of stylus
    lst = ret.stdout.decode("utf-8").split()
    try:
        x = lst.index('stylus')
        stylus_id = lst[x+2]
        process = subprocess.run('xsetwacom --set "' +stylus_id+ '" MapToOutput '
                                  + args.wacom, shell=True)
    except ValueError:
        print('Could not find tablet.\nOutput:' + str(ret.stdout.decode("utf-8"))
               + '\nError:'+ str(ret.stderr.decode("utf-8")))
elif args.setup:
    print('Not yet implemented')
elif args.wifi:
    ret = subprocess.run('yes '' | apt install linux-headers-$(uname -r)'
                          + ' build-essential', shell=True, capture_output=True,
                          check=True)
    print(ret.stdout.decode("utf-8"))
    rd = input("Clone repository? (Y/N) ")
    if rd == 'yes' or rd == 'y':
        subprocess.run('git clone git://github.com/lwfinger/rtw89.git' +
                       ' && cd rtw89 && make && make install', shell=True)
        rd = input("Load kernel module? (Y/N) ")
        if rd == 'yes' or rd == 'y':
            ret = subprocess.run('sudo modprobe -v rtw89pci', shell=True,
                                  capture_output=True)
            print(ret.stdout.decode("utf-8"))
            subprocess.run('rm -r rtw89', shell=True)
        else:
            subprocess.run('rm -r rtw89', shell=True)
elif args.audio:
    print('Open pavucontrol for volumcontrol gui')
    print('Alsamixer for tui with audiocontrols')
elif args.power:
    print('Status and system information: sudo tlp-stat -s')
    print('View configuration: sudo tlp-stat -c')
    print('View Battery report: sudo tlp-stat -b')
elif args.display:
    print('Duplicate screen to HDMI: xrandr --output HDMI-A-0 --auto --same-as eDP')
    print('Extend screen on HDMI: xrandr --output HDMI-A-0 --auto --right-of eDP')
    print('List all outputs: xrandr')
    print('Duplicate screen and adjust size to HDMI: xrandr --output eDP --primary --auto --output HDMI-A-0 --auto --same-as eDP')
