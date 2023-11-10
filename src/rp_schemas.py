INPUT_SCHEMA = {
    'prompt': {
        'type': str,
        'required': False,
    },
    'negative_prompt': {
        'type': str,
        'required': False,
        'default': None
    },
    # removed height and width
    'seed': {
        'type': int,
        'required': False,
        'default': None
    },
    'scheduler': {
        'type': str,
        'required': False,
        'default': 'DDIM'
    },
    'num_inference_steps': {
        'type': int,
        'required': False,
        'default': 25
    },
    'refiner_inference_steps': {
        'type': int,
        'required': False,
        'default': 50
    },
    'guidance_scale': {
        'type': float,
        'required': False,
        'default': 7.5
    },
    'strength': {
        'type': float,
        'required': False,
        'default': 0.3
    },
    'image_url': {
        'type': str,
        'required': False,
        'default': None
    },
    'num_images': {
        'type': int,
        'required': False,
        'default': 1,
        'constraints': lambda img_count: 3 > img_count > 0
    },
    # new variables
    'size':{
        'type': string,
        'default': 'small',
        'required': False,
        'constraints':  lambda item: item in ['small', 'medium', 'large']
    },
    'aspect_ratio':{
        'type': string,
        'default': '2:3',
        'required': False,
        'constraints': lambda item: item in ['3:2', '5:4', '1:1', '4:5','2:3']
    },    
    # for individual steps
    'hires_steps': {
        'type': int,
        'required': False,
        'default': 0,
        'constraints': lambda num_steps: 100 > num_steps > 0
    },
    'hires_denoising_strength': {
        'type': int,
        'required': False,
        'default': 0,
        'constraints': lambda num_steps: 100 > num_steps > 0
    },
    'upscale_by': {
        'type': float,
        'required': False,
        'default': 0,
        'constraints': lambda amt: 2 > amt > 0
    },
    'inpaint_face_denoising_strength': {
        'type': float,
        'required': False,
        'default': 0,
        'constraints': lambda str: 1 > str > 0.1
    },
    'inpaint_faces_width': {
        'type': int,
        'required': False,
    },
    'inpaint_faces_height': {
        'type': int,
        'required': False, 
    },  
    'inpaint_area': {
        'type': boolean,
        'required': False,
        'default': False
    },
    'control_net_enabled': {
        'type': boolean,
        'default': False,
        'required': False
    },
    'control_net_mode':{
        'type': string,
        'default': None,
        'required': False,
        'constraints': lambda str: str in ['canny','depth','pose']
    },
    'control_net_preprocessor':{
        'type': string,
        'default': None,
        'required': False,
    },
    'control_net_conditioning_scale':{
        'type': string,
        'default': 'small',
        'required': False,
        'constraints':  lambda item: item in ['small', 'medium', 'large']
    }
}
