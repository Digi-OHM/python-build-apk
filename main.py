import json
import uuid
import flet as ft

APP_TITLE = "Shopping List"
DATA_KEY = "shopping-data"
THEME_KEY = "shopping-theme"


LIGHT = {
    "bg": "#f5f5f5",
    "card": "#ffffff",
    "text": "#222222",
    "border": "#dddddd",
    "primary": "#4CAF50",
    "row_alt": "#f3f3f3",
    "thead_text": "#2e7d32",
    "input_bg": "#ffffff",
}

DARK = {
    "bg": "#121212",
    "card": "#1e1e1e",
    "text": "#eeeeee",
    "border": "#333333",
    "primary": "#3aa0ff",
    "row_alt": "#181818",
    "thead_text": "#66b2ff",
    "input_bg": "#1e1e1e",
}


def main(page: ft.Page):
    page.title = APP_TITLE
    page.padding = 0
    page.spacing = 0
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH

    state = {
        "items": [],
        "theme": "light",
    }

    def theme():
        return DARK if state["theme"] == "dark" else LIGHT

    def save_state():
        page.client_storage.set(DATA_KEY, json.dumps(state["items"]))
        page.client_storage.set(THEME_KEY, state["theme"])

    def load_state():
        raw_items = page.client_storage.get(DATA_KEY)
        raw_theme = page.client_storage.get(THEME_KEY)

        if raw_theme in ("light", "dark"):
            state["theme"] = raw_theme

        if raw_items:
            try:
                loaded = json.loads(raw_items)
                if isinstance(loaded, list):
                    state["items"] = loaded
            except Exception:
                state["items"] = []

    def sync_page_theme():
        t = theme()
        page.bgcolor = t["bg"]
        page.theme_mode = (
            ft.ThemeMode.DARK if state["theme"] == "dark" else ft.ThemeMode.LIGHT
        )

    title_text = ft.Text("🛒 Shopping List", size=22, weight=ft.FontWeight.BOLD)
    theme_switch = ft.Switch()
    name_input = ft.TextField(
        hint_text="Enter item...",
        expand=True,
        border_radius=14,
        border_color=LIGHT["border"],
        bgcolor=LIGHT["input_bg"],
        text_size=16,
        content_padding=ft.padding.symmetric(horizontal=16, vertical=14),
    )

    add_btn = ft.ElevatedButton("Add", width=130)
    reset_btn = ft.ElevatedButton("Reset", width=130)

    header_row = ft.Container()
    table_body = ft.Column(spacing=0, scroll=ft.ScrollMode.AUTO)
    table_holder = ft.Container()
    top_card = ft.Container(
        width=980,
        border_radius=18,
        padding=20,
        animate=300,
    )

    root = ft.Container(
        expand=True,
        padding=15,
        content=ft.Row(
            [top_card],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),
    )

    def apply_styles():
        t = theme()

        root.bgcolor = t["bg"]
        top_card.bgcolor = t["card"]
        title_text.color = t["text"]

        name_input.bgcolor = t["input_bg"]
        name_input.border_color = t["border"]
        name_input.color = t["text"]

        theme_switch.value = state["theme"] == "dark"

        header_row.bgcolor = ft.Colors.with_opacity(0.08, t["primary"])
        header_row.padding = ft.padding.symmetric(horizontal=12, vertical=14)
        header_row.border_radius = 0

        add_btn.style = ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=t["primary"],
            shape=ft.RoundedRectangleBorder(radius=14),
        )
        reset_btn.style = ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor="#999999",
            shape=ft.RoundedRectangleBorder(radius=14),
        )

    def render_table():
        t = theme()

        def on_note_change_factory(item_id):
            def on_change(e):
                for item in state["items"]:
                    if item["id"] == item_id:
                        item["note"] = e.control.value or ""
                        break
                save_state()
            return on_change

        def on_toggle_factory(item_id):
            def on_change(e):
                for item in state["items"]:
                    if item["id"] == item_id:
                        item["checked"] = bool(e.control.value)
                        break
                save_state()
                render()
            return on_change

        def on_delete_factory(item_id):
            def on_click(e):
                state["items"] = [
                    item for item in state["items"] if item["id"] != item_id
                ]
                save_state()
                render()
            return on_click

        header_row.content = ft.Row(
            [
                ft.Container(
                    ft.Text("No.", color=t["thead_text"], weight=ft.FontWeight.W_600),
                    width=60,
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    ft.Text("Name", color=t["thead_text"], weight=ft.FontWeight.W_600),
                    expand=4,
                    alignment=ft.alignment.center_left,
                ),
                ft.Container(
                    ft.Text("Note", color=t["thead_text"], weight=ft.FontWeight.W_600),
                    expand=4,
                    alignment=ft.alignment.center_left,
                ),
                ft.Container(
                    ft.Text("Status", color=t["thead_text"], weight=ft.FontWeight.W_600),
                    width=90,
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    ft.Text("Action", color=t["thead_text"], weight=ft.FontWeight.W_600),
                    width=100,
                    alignment=ft.alignment.center,
                ),
            ],
            spacing=0,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        rows = []
        for i, item in enumerate(state["items"], start=1):
            checked = bool(item.get("checked", False))
            row_bg = (
                ft.Colors.with_opacity(0.15, t["primary"])
                if checked
                else (t["row_alt"] if i % 2 == 0 else t["card"])
            )

            row = ft.Container(
                bgcolor=row_bg,
                animate=300,
                border=ft.border.only(bottom=ft.BorderSide(1, t["border"])),
                padding=ft.padding.symmetric(horizontal=12, vertical=8),
                content=ft.Row(
                    [
                        ft.Container(
                            ft.Text(str(i), color=t["text"]),
                            width=60,
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            ft.Text(
                                item.get("name", ""),
                                color=t["text"],
                                no_wrap=True,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                            expand=4,
                            alignment=ft.alignment.center_left,
                        ),
                        ft.Container(
                            ft.TextField(
                                value=item.get("note", ""),
                                border=ft.InputBorder.NONE,
                                dense=True,
                                text_size=14,
                                multiline=False,
                                bgcolor=t["card"],
                                color=t["text"],
                                content_padding=ft.padding.symmetric(horizontal=8, vertical=10),
                                on_change=on_note_change_factory(item["id"]),
                            ),
                            expand=4,
                        ),
                        ft.Container(
                            ft.Switch(
                                value=checked,
                                on_change=on_toggle_factory(item["id"]),
                            ),
                            width=90,
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            ft.IconButton(
                                icon=ft.icons.DELETE_OUTLINED,
                                icon_color="crimson",
                                tooltip="Delete",
                                on_click=on_delete_factory(item["id"]),
                            ),
                            width=100,
                            alignment=ft.alignment.center,
                        ),
                    ],
                    spacing=0,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            )
            rows.append(row)

        table_body.controls = rows
        table_holder.content = ft.Container(
            border=ft.border.all(1, t["border"]),
            border_radius=16,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            content=ft.Column(
                [header_row, table_body],
                spacing=0,
            ),
        )

    def render():
        sync_page_theme()
        apply_styles()
        render_table()
        page.update()

    def add_row(e):
        name = (name_input.value or "").strip()
        if not name:
            return

        state["items"].append(
            {
                "id": str(uuid.uuid4()),
                "name": name,
                "note": "",
                "checked": False,
            }
        )
        name_input.value = ""
        save_state()
        render()

    def reset_status(e):
        for item in state["items"]:
            item["checked"] = False
        save_state()
        render()

    def toggle_theme(e):
        state["theme"] = "dark" if theme_switch.value else "light"
        save_state()
        render()

    load_state()

    theme_switch.on_change = toggle_theme
    add_btn.on_click = add_row
    reset_btn.on_click = reset_status

    top_card.content = ft.Column(
        spacing=18,
        controls=[
            ft.Row(
                [title_text, theme_switch],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Row(
                [
                    name_input,
                    ft.Column(
                        [add_btn, reset_btn],
                        spacing=8,
                        tight=True,
                    ),
                ],
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
            table_holder,
        ],
    )

    page.add(root)
    render()


if __name__ == "__main__":
    ft.app(target=main)