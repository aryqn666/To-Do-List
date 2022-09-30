import collections.abc
import os
import click
import json


# Use command group in click. Make each if clause a command within that group. Define a sep function where each has
# its own options + arguments
@click.group()
def main():
    """ An application for managing tasks as a to-do list"""


@main.command('view')
@click.argument('identifier', required=False)
def view_todo(identifier):
    data: list[dict] = retrieve_todo_data()
    if identifier is None:
        comp_list(data)
    else:
        try:
            index = int(identifier)
            task = data[index - 1]
        except (ValueError, IndexError) as e:
            return
        print(f'{task["title"]}\n\n{task["body"]}')


# try to make these next functions command line activated like the view function. Can use it as basic framework
@main.command('add')
@click.argument('title')
@click.argument('body')
def add_todo(title, body):
    data: list[dict] = retrieve_todo_data()
    new_task = {f'title': title, 'body': body}
    data.append(new_task)
    persist_todo_data(data)
    comp_list(data)


@main.command('delete')
@click.argument('del_task', type=int)
def delete_todo(del_task):
    data: list[dict] = retrieve_todo_data()
    if len(data) == 0:
        print('Please add a task first')
    else:
        display_titles(data)
        try:
            num_to_del = int(del_task)
            del data[num_to_del - 1]
            persist_todo_data(data)
            comp_list(data)
        except (ValueError, IndexError) as e:
            print('Invalid task number')


@main.command('update')
@click.argument('num_task', type=int)
@click.argument('update_task', nargs=-1)
def update_todo(num_task, update_task):
    data: list[dict] = retrieve_todo_data()
    if len(data) == 0:
        print('Please add a task first')
    else:
        display_titles(data)
        while True:
            num_to_update = int(num_task)
            if num_to_update < len(data) + 1:
                break
        data[num_to_update - 1]['body'] = update_task
        persist_todo_data(data)
        comp_list(data)


def persist_todo_data(data):
    with open('saved.txt', "w") as f:
        json_string = json.dumps(list(data))
        f.write(json_string)
    print('List updated\n')


def display_titles(data):
    for i, title in enumerate(data, start=1):
        print(f'{i}. {title["title"]}')


def comp_list(data):
    print('Your TODO List:')
    for i, task in enumerate(data, start=1):
        print(f'{i}. {task["title"]} - {task["body"]}')


def retrieve_todo_data() -> list[dict]:
    # incase there is no file, this creates one and adds one task note pair
    if not os.path.exists('saved.txt') or os.stat('saved.txt').st_size == 0:
        return []
    else:
        with open('saved.txt', "r") as f:
            cont = json.loads(f.read())
            if isinstance(cont, collections.abc.Sequence):
                return cont
            else:
                return []


if __name__ == '__main__':
    main()
