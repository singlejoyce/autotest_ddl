# -*- coding: utf-8 -*-
from uiautomator import Device
import time
import os
from adb import ADB
from logger import Logger
from ConfigReader import ConfigReader


def skip_text_guide(d, step):  # 跳过文字引导 点击任意位置跳过
    x = config.getdic('text_guide')['touch_x']
    y = config.getdic('text_guide')['touch_y']
    mylogger.info('skip_text_guide...')
    for j in range(0, step):
        d.click(int(x), int(y))
    time.sleep(1)


def get_x_position(x):  # 根据当前设备分辨率转换x坐标值
    x = int(x) * int(width_high[0]) / int(standard_width)
    mylogger.info('get_x_position %s' % int(x))
    return int(x)


def get_y_position(y):  # 根据当前设备分辨率转换y坐标值
    y = int(y) * int(width_high[1]) / int(standard_high)
    mylogger.info('get_y_position %s' % int(y))
    return int(y)


def touch_level_up_pop(d):
    mylogger.info('touch_level_up_pop...')
    x = config.getdic('level_up_pop')['reward_confirm_button_x']
    y = config.getdic('level_up_pop')['reward_confirm_button_y']
    x2 = config.getdic('level_up_pop')['levelup_pop_close_button_x']
    y2 = config.getdic('level_up_pop')['levelup_pop_close_button_y']
    time.sleep(2)
    mylogger.info('reward_confirm_button...')
    d.click(get_x_position(x), get_y_position(y))  # 新手奖励框确定按钮
    time.sleep(2)
    mylogger.info('levelup_pop_close_button...')
    d.click(get_x_position(x2), get_y_position(y2))  # 等级升级框关闭按钮
    time.sleep(2)


def touch_back_button(d):
    mylogger.info('touch_back_button...')
    x = config.getdic('back_button')['back_button_x']
    y = config.getdic('back_button')['back_button_y']
    time.sleep(2)
    mylogger.info('back_button...')
    d.click(get_x_position(x), get_y_position(y))  # 点击返回按钮
    time.sleep(2)


def touch_pop_confirm_button_1(d):
    mylogger.info('touch_pop_confirm_button_1...')
    x = config.getdic('pop_confirm_button_1')['confirm_button1_x']
    y = config.getdic('pop_confirm_button_1')['confirm_button1_y']
    time.sleep(2)
    mylogger.info('confirm_button1...')
    d.click(get_x_position(x), get_y_position(y))  # 点击二次确认框中的确定按钮
    time.sleep(2)


def touch_pop_confirm_button_2(d):
    mylogger.info('touch_pop_confirm_button_2...')
    x = config.getdic('pop_confirm_button_2')['confirm_button2_x']
    y = config.getdic('pop_confirm_button_2')['confirm_button2_y']
    time.sleep(2)
    mylogger.info('confirm_button2...')
    d.click(get_x_position(x), get_y_position(y))  # 点击二次确认框中的确定按钮
    time.sleep(2)


def registered_login_creatrole(d):
    mylogger.info('wait...registered_login_creatrole...')
    x = config.getdic('registered_login_creatrole')['useragreement_confirm_x']
    y = config.getdic('registered_login_creatrole')['useragreement_confirm_y']
    x2 = config.getdic('registered_login_creatrole')['enter_game_button_x']
    y2 = config.getdic('registered_login_creatrole')['enter_game_button_y']
    x3 = config.getdic('registered_login_creatrole')['visitor_login_x']
    y3 = config.getdic('registered_login_creatrole')['visitor_login_y']
    x4 = config.getdic('registered_login_creatrole')['rolecreat_confirm_button_x']
    y4 = config.getdic('registered_login_creatrole')['rolecreat_confirm_button_y']
    time.sleep(2)
    mylogger.info('useragreement_confirm...')
    d.click(get_x_position(x), get_y_position(y))  # 点击用户协议确定按钮
    time.sleep(2)
    mylogger.info('enter_game_button...')
    d.click(get_x_position(x2), get_y_position(y2))  # 点击进入游戏按钮
    mylogger.info('visitor_login...')
    time.sleep(3)
    d.click(get_x_position(x3), get_y_position(y3))  # 点击限时体验按钮
    time.sleep(25)
    mylogger.info('rolecreat_confirm_button...')
    d.click(get_x_position(x4), get_y_position(y4))  # 点击注册角色界面中的创建按钮
    mylogger.info('wait...loading to new guide...')
    time.sleep(15)


def cloth_select(d):
    mylogger.info('wait...cloth_select...')
    x = config.getdic('cloth_select')['clothselect_confirm_x']
    y = config.getdic('cloth_select')['clothselect_confirm_y']
    time.sleep(2)
    skip_text_guide(d, 3)
    time.sleep(2)
    mylogger.info('clothselect_confirm...')
    d.click(get_x_position(x), get_y_position(y))  # 点击选衣服的确定按钮
    time.sleep(2)
    touch_pop_confirm_button_2(d)   # 二次确认框中确定按钮
    time.sleep(2)
    skip_text_guide(d, 1)
    time.sleep(2)
    touch_level_up_pop(d)  # 等级升级奖励框
    time.sleep(15)  # loading到世界地图


def dance_guide(d):
    mylogger.info('wait...dance_guide...')
    x = config.getdic('dance_guide')['lw_room_x']
    y = config.getdic('dance_guide')['lw_room_y']
    x2 = config.getdic('dance_guide')['creatroom_button_x']
    y2 = config.getdic('dance_guide')['creatroom_button_y']
    x3 = config.getdic('dance_guide')['creatroom_pop_confirm_button_x']
    y3 = config.getdic('dance_guide')['creatroom_pop_confirm_button_y']
    x4 = config.getdic('dance_guide')['room_start_dance_button_x']
    y4 = config.getdic('dance_guide')['room_start_dance_button_y']
    time.sleep(2)
    skip_text_guide(d, 2)
    time.sleep(2)
    mylogger.info('lw_room...')
    d.click(get_x_position(x), get_y_position(y))  # 点击恋舞大厅
    time.sleep(2)
    skip_text_guide(d, 1)
    time.sleep(2)
    mylogger.info('creatroom_button...')
    d.click(get_x_position(x2), get_y_position(y2))  # 点击创建房间按钮
    time.sleep(2)
    mylogger.info('creatroom_pop_confirm_button...')
    d.click(get_x_position(x3), get_y_position(y3))  # 点击创建房间pop框中确定按钮
    time.sleep(15)  # loading到房间内
    skip_text_guide(d, 1)
    time.sleep(2)
    mylogger.info('room_start_dance_button...')
    d.click(get_x_position(x4), get_y_position(y4))  # 点击房间内开始按钮
    time.sleep(160)  # loading到跳舞场景等待跳舞结束后回到房间内
    skip_text_guide(d, 1)
    time.sleep(2)
    touch_level_up_pop(d)  # 等级升级奖励框
    time.sleep(2)


def mall_guide(d):
    mylogger.info('wait...mall_guide...')
    x = config.getdic('mall_guide')['lw_mall_x']
    y = config.getdic('mall_guide')['lw_mall_y']
    x2 = config.getdic('mall_guide')['mall_item_x']
    y2 = config.getdic('mall_guide')['mall_item_y']
    x3 = config.getdic('mall_guide')['buy_button_x']
    y3 = config.getdic('mall_guide')['buy_button_y']
    x4 = config.getdic('mall_guide')['shopping_cart_x']
    y4 = config.getdic('mall_guide')['shopping_cart_y']
    x5 = config.getdic('mall_guide')['pay_button_x']
    y5 = config.getdic('mall_guide')['pay_button_y']
    time.sleep(2)
    skip_text_guide(d, 4)
    time.sleep(2)
    touch_back_button(d)  # 房间内返回按钮
    time.sleep(2)
    touch_pop_confirm_button_2(d)  # 二次确认框中确定按钮
    time.sleep(10)
    touch_back_button(d)  # 恋舞大厅返回按钮
    time.sleep(2)
    mylogger.info('lw_mall...')
    d.click(get_x_position(x), get_y_position(y))  # 恋舞商城
    time.sleep(2)
    touch_pop_confirm_button_1(d)  # 单个按钮pop框中确定按钮
    time.sleep(2)
    mylogger.info('mall_item...')
    d.click(get_x_position(x2), get_y_position(y2))  # 神秘天使
    time.sleep(2)
    mylogger.info('buy_button...')
    d.click(get_x_position(x3), get_y_position(y3))  # 购买按钮
    time.sleep(2)
    mylogger.info('shopping_cart...')
    d.click(get_x_position(x4), get_y_position(y4))  # 购物车按钮
    time.sleep(2)
    mylogger.info('pay_button...')
    d.click(get_x_position(x5), get_y_position(y5))  # 支付按钮
    time.sleep(2)
    touch_pop_confirm_button_2(d)  # 二次确认框中确定按钮
    time.sleep(2)
    touch_pop_confirm_button_1(d)  # 单个按钮pop框中确定按钮
    time.sleep(2)
    skip_text_guide(d, 2)
    time.sleep(2)
    touch_level_up_pop(d)  # 等级升级奖励框
    time.sleep(2)
    skip_text_guide(d, 2)
    time.sleep(2)
    touch_back_button(d)  # 商城返回按钮
    time.sleep(2)
    touch_pop_confirm_button_2(d)  # 二次确认框中确定按钮
    time.sleep(2)  # 返回到世界地图


def itembag_guide(d):
    mylogger.info('wait...itembag_guide...')
    x = config.getdic('itembag_guide')['itembag_x']
    y = config.getdic('itembag_guide')['itembag_y']
    x2 = config.getdic('itembag_guide')['itembag_item_x']
    y2 = config.getdic('itembag_guide')['itembag_item_y']
    x3 = config.getdic('itembag_guide')['save_button_x']
    y3 = config.getdic('itembag_guide')['save_button_y']
    time.sleep(2)
    mylogger.info('itembag...')
    d.click(get_x_position(x), get_y_position(y))  # 背包
    time.sleep(2)
    mylogger.info('itembag_item...')
    d.click(get_x_position(x2), get_y_position(y2))  # 神秘天使
    time.sleep(2)
    mylogger.info('save_button...')
    d.click(get_x_position(x3), get_y_position(y3))  # 保存搭配
    time.sleep(2)
    skip_text_guide(d, 1)
    time.sleep(2)
    touch_back_button(d)  # 背包返回按钮
    time.sleep(2)  # 返回到世界地图


def quest_guide(d):
    mylogger.info('wait...quest_guide...')
    x = config.getdic('quest_guide')['quest_x']
    y = config.getdic('quest_guide')['quest_y']
    x2 = config.getdic('quest_guide')['extension_quest_x']
    y2 = config.getdic('quest_guide')['extension_quest_y']
    x3 = config.getdic('quest_guide')['function_recommended_x']
    y3 = config.getdic('quest_guide')['function_recommended_y']
    time.sleep(2)
    skip_text_guide(d, 2)
    time.sleep(2)
    mylogger.info('quest...')
    d.click(get_x_position(x), get_y_position(y))  # 任务
    time.sleep(2)
    skip_text_guide(d, 1)
    time.sleep(1)
    mylogger.info('extension_quest...')
    d.click(get_x_position(x2), get_y_position(y2))  # 支线任务
    time.sleep(2)
    skip_text_guide(d, 1)
    time.sleep(2)
    mylogger.info('function_recommended...')
    d.click(get_x_position(x3), get_y_position(y3))  # 功能推荐
    time.sleep(2)
    skip_text_guide(d, 1)
    time.sleep(2)
    touch_level_up_pop(d)  # 等级升级奖励框
    time.sleep(2)
    skip_text_guide(d, 1)
    time.sleep(2)


def end_guide(d):
    mylogger.info('wait...last_guide...')
    x = config.getdic('end_guide')['res_download_cancel_x']
    y = config.getdic('end_guide')['res_download_cancel_x']
    time.sleep(2)
    skip_text_guide(d, 2)
    time.sleep(2)
    touch_back_button(d)  # 任务返回按钮
    time.sleep(2)
    touch_back_button(d)  # 任务返回按钮
    time.sleep(2)
    mylogger.info('res_download_cancel...')
    d.click(get_x_position(x), get_y_position(y))  # 资源下载框取消按钮
    time.sleep(2)


def do_test_case(device, deviceid):
    if not adb.is_install_app(deviceid, package_name):
        adb.install_app(deviceid, apkname)
    time.sleep(5)
    adb.start_activity(deviceid, component)
    adb.save_screenshot_img(deviceid)
    # 检查是否已完成解压，如果没有完成则等待
    while True:
        if adb.is_first_file_exist(deviceid, package_name):
            break
        else:
            mylogger.info('wait...unzip res...')
            time.sleep(60)
    mylogger.info('wait...loading to server list...')
    time.sleep(30)
    registered_login_creatrole(device)
    cloth_select(device)
    dance_guide(device)
    mall_guide(device)
    itembag_guide(device)
    quest_guide(device)
    end_guide(device)
    mylogger.info('test..end!')


if __name__ == '__main__':
    apkname = 'App/L5_518_All.apk'
    mylogger = Logger(logger='test_ddl').getlog()
    adb = ADB()
    config = ConfigReader(os.getcwd() + '/Config/Config.ini')
    standard_width = config.getdic('standard')['standard_width']
    standard_high = config.getdic('standard')['standard_high']
    mylogger.info('standard_width=%s, standard_high=%s' % (standard_width, standard_high))
    component = adb.get_app_package_info(apkname)
    package_name = component.split("/")[0]
    mylogger.info('component=%s' % component)
    devices_list = adb.find_devices()
    if devices_list:
        for i in range(len(devices_list)):
            mylogger.info('devices_list[%s]= %s' % (i, devices_list[i]))
            port_list = range(5555, 5555 + len(devices_list))
            test_device = Device(devices_list[i], port_list[i])
            width_high = adb.get_device_lcd_size(devices_list[i])
            mylogger.info('real_width=%s, real_high=%s' % (width_high[0], width_high[1]))
            do_test_case(test_device, devices_list[i])














