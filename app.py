import re

from shiny import App, ui, reactive, render, req
from beam_analysis import DistributedLoad, MomentConcentrated, PointLoad, main
from stretch import load_type, loads_input, stretch_ui

ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.div(
            ui.h5(f'Properties & Geometry :'),
            ui.input_text(id="inertia", label='Define moment of inetia I, unit m4',
                placeholder='ex. 0.0007'),

            ui.hr(),
            ui.input_text(id="span", label='Define length of each span, unit m',
                placeholder='ex. 5, 5, 4.5'),
            ui.input_action_button("button1", "Submit 1", class_="btn-primary"),

            ui.hr(),
            ui.input_text(id="support", label='Define support type, fixed=0, roller=1, pinned=2, free=3',
                placeholder='ex. 0, 1, 1, 2', value=None),
            ui.input_action_button("button2", "Submit 2", class_="btn-primary"),

            ui.hr(),
            #TODO help text
            ui.h5(f'Load Definition :'),
            ui.input_text(id="R0", label='Define external loads unit fy : N, M : N-m',
                placeholder='ex. 0, 0, -100, 25', value=None),
            ui.input_action_button("button3", "Submit 3", class_="btn-primary"),

            ui.hr(),
            ui.output_ui('output1'),
            ui.input_action_button("button4", "Submit 4", class_="btn-primary"),

            ui.hr(),
            ui.output_ui('output2'),
            ui.input_action_button("button5", "Submit 5", class_="btn-primary"),

            ui.hr(),
            ui.output_ui('output3'),
            ui.input_action_button("button6", "Submit 6", class_="btn-primary"),
            
    )
        ),
        ui.panel_main(
            ui.h5(f'Diagram :'),
            ui.hr(),
            ui.help_text(
                '''
                
                '''
            ),
            ui.output_plot(id="plot",)
        )
    )
)

def server(input, output, session):

    # span length
    @reactive.Calc()
    @reactive.event(input.button1) 
    def get_span():
        x = input.span()
        # TODO fix missed input type
        f = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", x)
        span = [float(n) for n in f]
        print(f"span = {input.span()}, m")
        return span

    # support type
    @reactive.Calc()
    @reactive.event(input.button2)
    def get_nodes():
        req(input.span())
        x = input.support()
        x = re.findall(r"([\d.]*\d+)", x)
        support = [int(n) for n in x]

        span = get_span()
        if len(support) != (len(span) + 1):
            print(f"We have {len(span) + 1} nodes, Try again!")
            App.close()

        for s in support:
            if s not in [0, 1, 2, 3] :
                # TODO aleart!
                print('support type not in [0, 1, 2, 3]')
                App.close()
                break
            else:
                pass
        print(f"Support Types : {input.support()}")
        return support

    # external load
    @reactive.Calc()
    @reactive.event(input.button3)
    def get_R0():
        req(input.support())
        x = input.R0()
        x = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", x)
        R0 = [int(n) for n in x]

        nodes = get_nodes()
        if len(R0) != (len(nodes)*2):
            print(f"We have {len(nodes)} nodes, We want {len(nodes)*2} values, Try again!")
            App.close()
        #TODO fix input type
        print(f"External Loads : {input.R0()}")
        return R0

    # loads in each stretch
    ## How many loads in stretch ..nth
    @reactive.Calc()
    def stretch_count():
        stretch = get_span()
        list = []
        for i in range(len(stretch)):
            list.append(stretch_ui('stretch_'+str(i+1))) # names stretch ID = stretch_1, stretch_2, ...
        return list

    ## display input box to define number of load for each stretch 
    @output 
    @render.ui
    @reactive.event(input.button3)
    def output1():
        st = stretch_count()
        return st

    ## Select load type for load ...nth
    @reactive.Calc()
    def loads():
        stretch = get_span()
        list = []
        # fetch quantity of loads of each stretch --> 1, 2, 3,...
        for i in range(len(stretch)): 
            quantities = input['stretch_'+str(i+1)]() # id comes from method stretch_count()
            for j in range(quantities): # define load type --> P, q, M
                list.append(load_type('stretch_'+str(i+1)+'_load_'+str(j+1))) # names load --> stretch_1_load_1, stretch_load_2
        
        return list

    ## display input box to define name of load type (P, q, M)
    @output 
    @render.ui
    @reactive.event(input.button4)
    def output2():
        load_name = loads()
        return load_name

    ## define loads values
    @reactive.Calc()
    def define_loads():
        stretch = get_span()
        list = []
        for i in range(len(stretch)): # nth stretchs
            quantities = input['stretch_'+str(i+1)]() # nth of loads for each stretch
            for j in range(quantities): # define value of each load 
                type = f'''stretch_{str(i+1)}_load_{str(j+1)}''' # stretch_1_load_1, stretch_1_load_2
                list.append(loads_input(input[type](), type))

        return list
            
    ## display input box to define value of each load
    @output 
    @render.ui
    @reactive.event(input.button5)
    def output3():
        load_def = define_loads()
        return load_def

    ## capture load value from user input
    @reactive.Calc()
    def load_capture():
        
        def calc_load(load_type, id):
            print(f'[INFO] Caluclating...with {id}')
            if load_type == 'P':
                value = input[id+'_p_v']()
                x = input[id+'_p_x']()
                P = PointLoad(float(value), float(x))#, Down+ Up-
                print(f'[INFO]--->{P}')
                return P
            elif load_type == 'q':
                value = input[id+'_q_v']()
                start = input[id+'_q_s']()
                length = input[id+'_q_l']()
                q = DistributedLoad(float(value), float(start), float(length))#, Down+ Up-
                print(f'[INFO]--->{q}')
                return q
            else:
                value = input[id+'_m_v']()
                x = input[id+'_m_x']()
                m = MomentConcentrated(float(value), float(x))# counterclockwise +
                print(f'[INFO]--->{m}')
                return m

        stretch = get_span()
        f = [[] for i in range(len(stretch))]
        for i in range(len(stretch)): # nth stretchs
            quantities = input['stretch_'+str(i+1)]() # nth of loads for each stretch
            for j in range(quantities):
                print(len(f[i]))
                type = f'''stretch_{str(i+1)}_load_{str(j+1)}''' # stretch_1_load_1, stretch_1_load_2
                print(type)
                print(input[type]())  
                f[i].append(calc_load(input[type](), type))

        return f

    @output
    @render.plot
    @reactive.event(input.button6)
    def plot():
        spans = get_span()
        nodes = get_nodes()
        R0 = get_R0()
        loads= load_capture()

        print(*spans)
        print(*nodes)
        print(*R0)

        for i in range(0, len(loads)):
            print(f'Load in stretch {i+1} : ')
            print(*loads[i], sep = "\n")

        E = 200 # GPa
        I = float(input.inertia())

        fig = main(E, I, spans, nodes, loads, R0)
        return fig

app = App(ui, server)


## How to use
## shiny run --reload app.py