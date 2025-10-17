from fasthtml.common import *

def render(todo):
    tid = f'todo-{todo.id}'
    toggle = A('Toggle', hx_get=f'/toggle/{todo.id}', target_id=tid)
    delete = A('Delete', hx_delete=f'/{todo.id}', 
               hx_swap='outerHTML', target_id=tid)
    return Li(toggle, delete, 
              todo.titles + (' x' if todo.done else ''), 
              id=tid)


app,rt,todos,Todo = fast_app('todos.db', live=False, render=render, 
                               id=int, titles=str, done=bool, pk='id')

@rt("/")
def get():
    frm = Form(Group(mk_input(), 
                     Button("Add")), 
                     hx_post='/', target_id='todo-list', hx_swap='beforeend')
    # todos.insert(Todo(titles="Third todo", done=False))
    return Titled("Todos",
                    Card( 
                        Ul(*todos(), id='todo-list'),
                        header=frm
                    )
                )

def mk_input():
    return Input(placeholder='Add a new todo', id='titles', hx_swap_oob='true') # fasthtml creates auto creates name variable same as id 

@rt("/")
def post(todo:Todo): 
    return todos.insert(todo), mk_input()


@rt("/{tid}")
def delete(tid:int): 
    todos.delete(tid)

@rt("/toggle/{tid}")
def get(tid:int):
    todo = todos[tid]
    todo.done = not todo.done
    todos.update(todo)
    return todo

serve()
