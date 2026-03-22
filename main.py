import flet as ft
import os

def generate_static_html():
    """สร้างไฟล์ HTML จำลองหน้าตา UI (แบบ Static)"""
    html_content = """
    <!DOCTYPE html>
    <html lang="th">
    <head>
        <meta charset="UTF-8">
        <title>Minimal Task Demo</title>
        <style>
            body { font-family: sans-serif; background: #f4f4f9; display: flex; justify-content: center; padding: 20px; }
            .card { background: white; width: 100%; max-width: 400px; padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
            .header { display: flex; justify-content: space-between; align-items: center; }
            .input-box { display: flex; gap: 10px; margin: 20px 0; }
            input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 8px; }
            button { background: #2196F3; color: white; border: none; padding: 10px 15px; border-radius: 8px; cursor: pointer; }
            .item-card { border: 1px solid #eee; padding: 10px; border-radius: 10px; margin-top: 10px; }
        </style>
    </head>
    <body>
        <div class="card">
            <div class="header"><h2>My Tasks</h2></div>
            <div class="input-group">
                <input type="text" placeholder="What needs to be done?">
                <button>Add</button>
            </div>
            <div class="item-card">
                <strong>Example Task</strong><br>
                <small>This is a static preview.</small>
            </div>
        </div>
    </body>
    </html>
    """
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("✨ สร้างไฟล์ index.html สำเร็จ! (Static Preview)")

def main(page: ft.Page):
    page.title = "Minimal Task Tracker"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)

    my_data = []

    # UI Components
    items_container = ft.Column(spacing=10, scroll=ft.ScrollMode.ADAPTIVE)
    name_input = ft.TextField(label="Task Name", expand=True, border_radius=10)

    def render_items():
        items_container.controls.clear()
        for i, item in enumerate(my_data):
            items_container.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(item["name"], weight="bold"),
                            ft.IconButton(ft.Icons.DELETE, icon_color="red", on_click=lambda e, idx=i: delete_item(idx))
                        ], alignment="spaceBetween"),
                        ft.TextField(value=item["note"], label="Note", border="underline")
                    ]),
                    padding=10, border=ft.border.all(1, "#eee"), border_radius=10
                )
            )
        page.update()

    def delete_item(index):
        my_data.pop(index)
        render_items()

    def add_clicked(e):
        if name_input.value:
            my_data.append({"name": name_input.value, "note": "", "status": False})
            name_input.value = ""
            render_items()

    page.add(
        ft.Row([
            ft.Text("My Tasks", size=25, weight="bold"),
            ft.IconButton(ft.Icons.DARK_MODE, on_click=lambda _: setattr(page, "theme_mode", 
                ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT) or page.update())
        ], alignment="spaceBetween"),
        ft.Row([name_input, ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=add_clicked)]),
        items_container
    )

if __name__ == "__main__":
    # ถ้าไม่ได้รันบน GitHub ให้สร้างไฟล์ HTML ทิ้งไว้ด้วย
    if not os.environ.get("GITHUB_ACTIONS"):
        generate_static_html()
    
    # รันแอปปกติ
    ft.app(target=main)