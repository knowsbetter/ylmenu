import json
import time

import httpx
import openpyxl

from taskworker import config
from taskworker.schemas.schemas import DishBase, MenuBase, SubmenuBase

# ready_to_check_changes = False


def excel_to_json():
    # Загрузка данных из файла XLSX
    xlsx_file = 'taskworker/admin/Menu.xlsx'
    wb = openpyxl.load_workbook(xlsx_file)
    sheet = wb.active

    # Преобразование данных во вложенную структуру
    current_menu = None
    current_submenu = None
    menu_data = []
    submenu_data = []
    dish_data = []
    submenu_id = 0
    dish_id = 0
    submenus_for_menu_count = 0
    dishes_for_menu_count = 0
    dishes_for_submenu_count = 0

    for row in sheet.iter_rows(values_only=True):
        a_col, b_col, c_col, d_col, e_col, f_col = row
        if a_col:
            if current_menu:
                current_menu.submenus_count = submenus_for_menu_count
                current_menu.dishes_count = dishes_for_menu_count
                menu_data.append(current_menu.model_dump())
                submenus_for_menu_count = 0
                dishes_for_menu_count = 0
            current_menu = MenuBase(id=str(a_col))
            current_menu.title = b_col
            current_menu.description = c_col
        elif b_col:
            if current_submenu:
                current_submenu.dishes_count = dishes_for_submenu_count
                submenu_data.append(current_submenu.model_dump())
                dishes_for_submenu_count = 0
            submenu_id += 1
            submenus_for_menu_count += 1
            current_submenu = SubmenuBase(id=str(submenu_id))
            current_submenu.title = c_col
            current_submenu.description = d_col
            current_submenu.menu_id = current_menu.id
        elif c_col:
            dish_id += 1
            dishes_for_menu_count += 1
            dishes_for_submenu_count += 1
            current_dish = DishBase(id=str(dish_id))
            current_dish.title = d_col
            current_dish.description = e_col
            current_dish.price = str(f_col)
            current_dish.submenu_id = current_submenu.id
            current_dish.menu_id = current_menu.id
            dish_data.append(current_dish.model_dump())

    current_submenu.dishes_count = dishes_for_submenu_count
    submenu_data.append(current_submenu.model_dump())
    current_menu.submenus_count = submenus_for_menu_count
    current_menu.dishes_count = dishes_for_menu_count
    menu_data.append(current_menu.model_dump())

    admin_menu = [menu_data, submenu_data, dish_data]

    return admin_menu


def write_to_json(data):
    with open('taskworker/output/menu.json', 'w+', encoding='utf-8') as f:
        json.dump(data, f)


def find_changes():
    #    if ready_to_check_changes:
    with open('taskworker/output/menu.json', encoding='utf-8') as file:
        original_data = json.load(file)
    discrepancies = []
    updated_data = excel_to_json()

    for i, original_list in enumerate(original_data):
        for j, original_item in enumerate(original_list):
            if list(original_item.values()) != list((updated_data[i][j]).values()):
                discrepancies.append(updated_data[i][j])

    print(discrepancies)
    send_updated_items(discrepancies)
    write_to_json(updated_data)


def send_updated_items(list_of_updates):
    for item in list_of_updates:
        if 'submenus_count' in item.keys():
            message = {'title': item['title'], 'description': item['description']}
            with httpx.Client(base_url=config.LOCAL_HOST) as client:
                response = client.patch(f"/api/v1/menus/{item['id']}", json=message)
                print(response)
        elif 'submenu_id' in item.keys():
            message = {'title': item['title'], 'description': item['description', 'price': item['price']]}
            with httpx.Client(base_url=config.LOCAL_HOST) as client:
                response = client.patch(
                    f"/api/v1/menus/{item['menu_id']}/submenus/{item['submenu_id']}/dishes/{item['id']}", json=message)
                print(response)
        else:
            message = {'title': item['title'], 'description': item['description']}
            with httpx.Client(base_url=config.LOCAL_HOST) as client:
                response = client.patch(f"/api/v1/menus/{item['menu_id']}/submenus/{item['id']}", json=message)
                print(response)


def signal_to_update_db():
    time.sleep(5)
    message = {'detail': 'start_update'}
    with httpx.Client(base_url=config.LOCAL_HOST) as client:
        response = client.post('/api/v1/admin/fill_db_from_json/', json=message)
        print(response)
