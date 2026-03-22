import flet as ft

def main(page: ft.Page):
    page.title = "Mobile Table APK"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.ADAPTIVE

    # Data Storage (Local list)
    my_data = []

    # UI Components
    name_input = ft.TextField(label="Item Name", expand=True)
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("No.")),
            ft.DataColumn(ft.Text("Name")),
            ft.DataColumn(ft.Text("Note")),
            ft.DataColumn(ft.Text("Status")),
            ft.DataColumn(ft.Text("Action")),
        ],
        rows=[]
    )

    def delete_item(e, index):
        my_data.pop(index)
        render_table()

    def render_table():
        table.rows.clear()
        for i, item in enumerate(my_data):
            table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(i + 1))),
                        ft.DataCell(ft.Text(item["name"])),
                        ft.DataCell(ft.TextField(value=item["note"], border=ft.InputBorder.NONE)),
                        ft.DataCell(ft.Switch(value=item["status"])),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.icons.DELETE_OUTLINE,
                                icon_color="red",
                                on_click=lambda e, idx=i: delete_item(e, idx)
                            )
                        ),
                    ]
                )
            )
        page.update()

    def add_clicked(e):
        if name_input.value:
            my_data.append({"name": name_input.value, "note": "", "status": False})
            name_input.value = ""
            render_table()

    # Layout
    page.add(
        ft.Row([name_input, ft.ElevatedButton("Add", on_click=add_clicked)]),
        ft.Divider(),
        ft.Column([table], scroll=ft.ScrollMode.ALWAYS)
    )

ft.app(target=main)