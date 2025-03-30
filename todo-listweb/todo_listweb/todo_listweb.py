"""Welcome to Reflex! This file outlines the steps to create a basic app."""
from datetime import datetime

import reflex as rx


# Define the Task model
class Task(rx.Base):
    """Task model."""
    task: str
    notes: str
    due_date: datetime
    status: str



# Define the State
class State(rx.State):
    tasks: list[Task] = [
        Task(task="Example Task", notes="This is an example", due_date= datetime(2025, 3, 24), status = "In Progress"),
    ]

    def add_task(self, form_data: dict):
        """Add a new task."""
        self.tasks.append(Task(**form_data))

    def delete_task(self, task_to_delete: Task):
        """Delete a task."""
        self.tasks = [task for task in self.tasks if task != task_to_delete]


        


def _badge(icon: str, text: str, color_scheme: str):
    return rx.badge(
        rx.icon(icon, size=16),
        text,
        color_scheme=color_scheme,
        radius="full",
        variant="soft",
        size="3",
    )

def status_badge(status: str):
    badge_mapping = {
        "Completed": ("check", "Completed", "green"),
        "In Progress": ("loader", "In Progress", "yellow"),
        "Not Started": ("ban", "Not Started", "red"),
    }
    return _badge(*badge_mapping.get(status, ("loader", "In progress", "yellow")))
# Component to show individual task rows
def show_task(task: Task):
    return rx.table.row(
        rx.table.cell(task.task),
        rx.table.cell(task.notes),
        rx.table.cell(task.due_date),
        rx.table.cell(
            rx.match(
                task.status,
                ("Completed", status_badge("Completed")),
                ("In Progress", status_badge("In Progress")),
                ("Not Started", status_badge("Not Started")),
                status_badge("Not Started"),
            )
        ),  # Close the status cell
        rx.table.cell(  # Separate cell for actions
            rx.hstack(
                rx.button(
                    "Edit",
                    color_scheme="blue",
                    size="2"
                ),
                rx.button(
                    "Delete",
                    color_scheme="red",
                    size="2",
                    on_click=lambda: State.delete_task(task),
                ),
                spacing="2",
            )
        )  # Close the actions cell
    )  # Close the row
def add_task_form():
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus"),
                "Add Task",
                color_scheme="green",
                size="2"
            ),
        ),
        rx.dialog.content(
            rx.dialog.title("Add New Task"),
            rx.dialog.description(
                "Fill in the task details"
            ),
            rx.form(
                rx.vstack(
                    rx.input(
                        placeholder="Enter a Task",
                        name="task",
                        required=True
                    ),
                    rx.input(
                        placeholder="Notes",
                        name="notes",
                    ),
                    rx.input(
                        type ="date",
                        name="due_date",

                    ),
                    rx.select(
                        ["Completed", "In Progress", "Not Started"],
                        placeholder="Status",
                        name="status",
                    ),
                    rx.hstack(
                        rx.dialog.close(
                            rx.button(
                                "Cancel",
                                color_scheme="gray",
                                size="2"
                            ),
                        ),
                        rx.dialog.close(
                            rx.button(
                                "Add",
                                type_="submit",
                                color_scheme="green",
                                size="2"
                            ),
                        ),
                        spacing="3",
                    ),
                    spacing="4",
                ),
                on_submit=State.add_task,
                reset_on_submit=True,
            ),

            max_width="450px",
            padding="1.5em",
            border=f"2px solid {rx.color('accent', 7)}",
            border_radius="25px",
        ),
    )

def task_table():
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell(
                    rx.hstack(
                        rx.icon("logs"),
                        "Task",
                        spacing="2"
                    )
                ),
                rx.table.column_header_cell(
                    rx.hstack(
                        rx.icon("notebook-pen"),
                        "Notes",
                        spacing = "2"
                    )
                ),
                rx.table.column_header_cell(
                    rx.hstack(
                        rx.icon("calendar-clock"),
                        "Date",
                        spacing = "2"
                    )
                ),

                rx.table.column_header_cell(
                    rx.hstack(
                        rx.icon("chart-bar-big"),
                        "Status",
                        spacing="2"
                    )
                ),

                rx.table.column_header_cell(
                    rx.hstack(
                        rx.icon("cog"),
                        "Actions",
                        spacing = "2"
                    )
                ),
            ),
        ),
        rx.table.body(
            rx.foreach(
                State.tasks,
                show_task,
            ),
        ),
        variant="surface",
        size="3",
        width="100%",
    )


def navbar():
    return rx.flex(
        rx.badge(
            rx.icon(tag="list-todo", size=28),
            rx.heading("Welcome to your To-Do List", size="6"),
            color_scheme="green",
            radius="large",
            align="center",
            variant="surface",
            padding="0.65rem",
        ),
        rx.spacer(),
        rx.hstack(
            rx.heading("Screen Mode : ", size = "2"),
            rx.color_mode.button(),
            align="center",
            spacing="3",
        ),
        spacing="2",
        flex_direction=["column", "column", "row"],
        align="center",
        width="100%",
        top="0px",
        padding_top="2em",
    )


def index():
    return rx.vstack(
        navbar(),
        add_task_form(),
        task_table(),
        width="100%",
        spacing="6",
        padding_x=["1.5em", "1.5em", "3em"],
    )

# Create the app and add the page
app = rx.App(
    theme=rx.theme(
        appearance="dark", has_background=True, radius="large", accent_color="indigo"
    ),
)

app.add_page(index)