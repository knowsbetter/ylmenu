from pydantic import BaseModel


class MenuBase(BaseModel):
    """Scheme for menu item creation"""

    id: str
    title: str = ''
    description: str = ''
    submenus_count: int = 0
    dishes_count: int = 0


class SubmenuBase(BaseModel):
    """Scheme for menu item creation"""

    id: str
    title: str = ''
    description: str = ''
    dishes_count: int = 0
    menu_id: str = ''


class DishBase(BaseModel):
    """Scheme for menu item creation"""

    id: str
    title: str = ''
    description: str = ''
    price: str = ''
    menu_id: str = ''
    submenu_id: str = ''
