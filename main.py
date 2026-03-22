import flet as ft

def main(page: ft.Page):
    page.title = "Shopping List"
    page.padding = 0

    # 🔄 loading กลางจอ
    loader = ft.Container(
        content=ft.ProgressRing(),
        alignment=ft.alignment.center,
        expand=True,
        visible=True
    )

    web = ft.WebView(
        url="index.html",
        expand=True,
        visible=False,  # 🔴 ซ่อนไว้ก่อน

        on_page_started=lambda e: show_loader(),
        on_page_ended=lambda e: hide_loader(),
    )

    def show_loader():
        loader.visible = True
        web.visible = False
        page.update()

    def hide_loader():
        loader.visible = False
        web.visible = True
        page.update()

    # 📦 stack ซ้อนกัน
    page.add(
        ft.Stack([
            web,
            loader
        ])
    )


if __name__ == "__main__":
    ft.app(target=main, assets_dir=".")