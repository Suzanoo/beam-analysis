from shiny import  ui, Inputs

from beam_analysis import DistributedLoad, MomentConcentrated, PointLoad

def stretch_ui(id):
    return (ui.div(
        ui.h6(f'How many loads in {id} ?'),
        ui.input_numeric(id=id, label="", value=1, min=1, max=100)
    )
    )
    
def load_type(id):
    return(ui.div(
        ui.input_select(
            id,
            f'Select load type for : {id}',
            {
                'P' : 'P',
                'q' : 'q',
                'M' : 'M'            }
        )
    ))

def point_load(id):
    return(ui.div(
        ui.h5(f'Load for {id}'),
        ui.input_text(id=id+"_p_x", label='Position in m', placeholder='ex. 2.5', value=None),
        ui.input_text(id=id+"_p_v", label='Value in N, -up, +down', placeholder='ex. 5000', value=None),
    ))

def line_load(id):
    return(ui.div(
        ui.h5(f'Load for {id}'),
        ui.input_text(id=id+"_q_s", label='Start position in m', placeholder='ex. 0', value=None),
        ui.input_text(id=id+"_q_l", label='Length of q in m', placeholder='ex. 5', value=None),
        ui.input_text(id=id+"_q_v", label='Value in N/m, -up, +down', placeholder='ex. 5000', value=None),

    ))

def moment(id):
    return(ui.div(
        ui.h5(f'Define for {id}'),
        ui.input_text(id=id+"_m_x", label='Position in m', placeholder='ex. 2.5', value=None),
        ui.input_text(id=id+"_m_v", label='Value in N-m, +counter clockwise, -clockwise', placeholder='ex. 5000', value=None),
    ))

def loads_input(load_type, id):
    if load_type == 'P':
        return point_load(id)
    elif load_type == 'q':
        return line_load(id)
    else:
        return moment(id)
