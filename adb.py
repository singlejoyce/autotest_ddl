# -*- coding: utf-8 -*-
__author__ = "joyce"

import os
import platform
import re
import time
from logger import Logger
import subprocess


class ADB(object):
    def __init__(self):
        self.adblogger = Logger(logger='adbUtils').getlog()

        # 判断系统类型，windows使用findstr，linux使用grep
        system = platform.system()
        if system is "Windows":
            self.find_util = "findstr"
        else:
            self.find_util = "grep"

    def cmd(self, args):
        """
        cmd命令
        args:adb devices
        return type：str
        """
        cmd = "%s" % str(args)
        return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) \
            .stdout.read().strip().decode('utf-8')

    def cmd_return_list(self, args):
        """
        cmd命令
        args:adb devices
        return type：list
        """
        cmd = "%s" % str(args)
        return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) \
            .stdout.readlines()

    def find_devices(self):
        """
        获得连接的设备（包括真机和虚拟机，原则上可以多台机器同时测试）
        devices_list = find_devices()
        """
        try:
            devices = re.findall(r'(.*?)\s+device', self.cmd("adb devices"))
            if len(devices) > 1:
                deviceids = devices[1:]
                self.adblogger.info('total find %s device(s)' % str(len(devices) - 1))
                for i in deviceids:
                    self.adblogger.info('deviceids:%s' % i)
                return deviceids
            else:
                self.adblogger.error('find devices failed,pls check!')
                return
        except Exception as e:
            self.adblogger.error("-----socket timeout------")

    def get_android_version(self, args):
        """
        获取设备中的Android版本号，如4.2.2
        """
        android_version = self.cmd('adb -s %s shell getprop ro.build.version.release' % args)
        return android_version

    def get_sdk_version(self, args):
        """
        获取设备SDK版本号
        """
        sdk_version = self.cmd('adb  -s %s shell getprop ro.build.version.sdk' % args)
        return sdk_version

    def get_device_model(self, args):
        """
        获取设备型号
        """
        device_model = self.cmd('adb  -s %s shell getprop ro.product.model' % args)
        return device_model

    def get_device_lcd_size(self, args):
        """
        获取设备屏幕分辨率，return (width, high)
        """
        out = self.cmd('adb -s %s shell dumpsys display | %s PhysicalDisplayInfo' % (args, self.find_util))
        if not out:
            display = re.split(':|x| ', self.cmd('adb -s %s shell wm size' % args))  # 这种方法适用高通平台
        else:
            display = re.compile(r'\d+').findall(out)
        return display

    def get_app_package_info(self, appfile):
        """
        获取apk内的包名和Activity，返回的字符串格式为：com.ddianle.lovedance.ddl/com.ddianle.activity.MainActivity
        """
        info = self.cmd('aapt dump badging %s' % appfile)
        package_name = re.compile(r'package: name=\'(.*?)\'').findall(info)[0]
        main_activity = re.compile(r'launchable-activity: name=\'(.*?)\'').findall(info)[0]
        component = package_name + '/' + main_activity
        return component

    def install_app(self, args, appfile):
        """
        安装app，app名字不能含中文字符
        args:
        - appFile -: app路径
        usage: install("\\apps\\L5_518_All.apk")
        """
        self.cmd('adb -s %s install -r %s' % (args, appfile))

    def remove_app(self, args, packagename):
        """
        卸载应用
        args:
        - packagename -:应用包名，非apk名
        """
        self.cmd('adb -s %s uninstall %s' % (args, packagename))

    def start_activity(self, args, cmp):
        """
        启动一个Activity
        usage: startActivity(component = "com.ddianle.lovedance.ddl/com.ddianle.activity.MainActivity")
        """
        self.cmd('adb -s %s shell am start -n %s' % (args, cmp))

    def reboot(self, args):
        """
        重启设备
        """
        self.cmd('adb -s %s reboot' % args)

    def get_system_applist(self, args):
        """
        获取设备中安装的系统应用包名列表
        """
        sysapp = []
        for packages in self.cmd_return_list('adb -s %s shell pm list packages -s' % args):
            sysapp.append(packages.strip().decode('utf-8').split(":")[-1].splitlines()[0])

        return sysapp

    def get_third_applist(self, args):
        """
        获取设备中安装的第三方应用包名列表
        """
        thirdapp = []
        for packages in self.cmd_return_list('adb -s %s shell pm list packages -3' % args):
            thirdapp.append(packages.strip().decode('utf-8').split(":")[-1].splitlines()[0])

        return thirdapp

    def get_matching_applist(self, args, keyword):
        """
        模糊查询与keyword匹配的应用包名列表
        usage: get_matching_applist("ddl")
        """
        matapp = []
        for packages in self.cmd_return_list('adb -s %s shell pm list packages %s' % (args, keyword)):
            matapp.append(packages.strip().decode('utf-8').split(":")[-1].splitlines()[0])

        return matapp

    def is_install_app(self, args, packagename):
        """
        判断应用是否安装，已安装返回True，否则返回False
        usage: isInstall("com.ddianle.lovedance.ddl")
        """
        if self.get_matching_applist(args, packagename):
            return True
        else:
            return False

    def clear_app_data(self, args, packagename):
        """
        清除应用用户数据
        usage: clearAppData("com.android.contacts")
        """
        if "Success" in self.cmd('adb -s %s shell pm clear %s' % (args, packagename)).splitlines():
            return "clear user data success "
        else:
            return "make sure package exist"

    def reset_current_app(self, args):
        """
        重置当前应用
        """
        self.clear_app_data(self.get_current_packagename(args))
        self.start_activity(self.get_focused_package_and_activity(args))

    def get_focused_package_and_activity(self, args):
        """
        获取当前应用界面的包名和Activity，返回的字符串格式为：packageName/activityName
        """
        # pattern = re.compile(r'name=(.*?),')
        pattern = re.compile(r"[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+")
        out = self.cmd('adb -s %s shell dumpsys window w | %s name= | %s \/ ' % (args, self.find_util, self.find_util))
        return pattern.findall(out)[0]

    def get_current_packagename(self, args):
        """
        获取当前运行的应用的包名
        """
        return self.get_focused_package_and_activity(args).split("/")[0]

    def get_current_activity(self, args):
        """
        获取当前运行应用的activity
        """
        return self.get_focused_package_and_activity(args).split("/")[-1]

    def get_start_total_time(self, args, cmp):
        """
        获取启动应用所花时间
        usage: getAppStartTotalTime("com.ddianle.lovedance.ddl/com.ddianle.activity.MainActivity")
        """
        start_time = \
        self.cmd('adb -s %s shell am start -W %s | %s TotalTime' % (args, cmp, self.find_util)).split(": ")[-1]
        return int(start_time)

    def get_pid(self, args, packagename):
        """
        获取进程pid
        args:
        - packageName -: 应用包名
        usage: getPid("com.ddianle.lovedance.ddl")
        """

        pidinfo = self.cmd('adb -s %s shell ps | %s %s$' % (args, self.find_util, packagename))
        if pidinfo == '':
            return "the process doesn't exist."

        pattern = re.compile(r"\d+")
        result = pidinfo.split(" ")
        result.remove(result[0])

        return pattern.findall(" ".join(result))[0]

    def kill_process(self, args, pid):
        """
        杀死应用进程
        args:
        - pid -: 进程pid值
        usage: killProcess(154)
        注：杀死系统应用进程需要root权限
        """
        if self.cmd('adb -s %s shell kill %s' % (args, str(pid))).split(": ")[-1] == "":
            return "kill success"
        else:
            return self.cmd('adb -s %s shell kill %s' % (args, str(pid))).split(": ")[-1]

    def quit_app(self, args, packagename):
        """
        退出app，类似于kill掉进程
        usage: quitApp("com.ddianle.lovedance.ddl")
        """
        self.cmd('adb -s %s shell am force-stop %s' % (args, packagename))

    def get_battery_level(self, args):
        """
        获取电池电量
        """
        level = self.cmd('adb -s %s shell dumpsys battery | %s level' % (args, self.find_util)).split(": ")[-1]

        return int(level)

    def get_battery_status(self, args):
        """
        获取电池充电状态
        BATTERY_STATUS_UNKNOWN：未知状态
        BATTERY_STATUS_CHARGING: 充电状态
        BATTERY_STATUS_DISCHARGING: 放电状态
        BATTERY_STATUS_NOT_CHARGING：未充电
        BATTERY_STATUS_FULL: 充电已满
        """
        status_dict = {1: "BATTERY_STATUS_UNKNOWN",
                       2: "BATTERY_STATUS_CHARGING",
                       3: "BATTERY_STATUS_DISCHARGING",
                       4: "BATTERY_STATUS_NOT_CHARGING",
                       5: "BATTERY_STATUS_FULL"}
        status = self.cmd('adb -s %s shell dumpsys battery | %s status' % (args, self.find_util)).split(": ")[-1]

        return status_dict[int(status)]

    def get_battery_temp(self, args):
        """
        获取电池温度
        """
        temp = self.cmd('adb -s %s shell dumpsys battery | %s temperature' % (args, self.find_util)).split(": ")[-1]

        return int(temp) / 10.0

    def is_first_file_exist(self, args, packagename):
        """
        判断应用是否解压完资源，已解压返回True，否则返回False
        usage: is_first_file_exist()
        """
        file_path = '/sdcard/Android/data/' + packagename + '/files/xuanqu/lwts/config/'
        temp = self.cmd('adb -s %s shell ls %s | %s isFirst' % (args, file_path, self.find_util))

        if temp:
            return True
        else:
            return False

    def save_screenshot_img(self, args):
        """
        保存截图到本地screenshot文件夹
        """
        screenshot_dir = os.getcwd() + '/Screenshot/'
        # 格式化时间戳为20180107-001542形式
        ts = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        if not os.path.isdir(screenshot_dir):
            os.mkdir(screenshot_dir)
        self.cmd('adb -s %s shell screencap -p /sdcard/temp.png' % args)
        # 本地图片命名格式为Screenshot_20180107-002134.png
        self.cmd('adb -s %s pull /sdcard/temp.png %s' % (args, '{}{}.png'.format(screenshot_dir, ('Screenshot_' + ts))))
        self.cmd('adb -s %s shell rm /sdcard/temp.png' % args)
