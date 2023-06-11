import os

from utils import *

def main():
    operating_system = get_os()
    env_check()
    server_apikey_exists = True if len(env_api_key) > 0 else False
    server_custom_models = num_custom_models = 0
    included_models = len(available_models)

    if isinstance(env_custom_models, list):
        server_custom_models = num_custom_models = len(env_custom_models)

#    port_check_result = bool(port_check(env_listen_port))
    port_check_result = True
    cls()
    print(BU_text('vits_tts_listener by AznIronMan'))
    blank_line()
    print(f'{B_text("Server Name:")}{C_text(env_listen_name,"cyan")}',f'Server Address: {env_listen_host}:{env_listen_port}{web_tts_route}', sep='\t')
    blank_line()
    print(f'Server API Key On: {YN_to_TF(server_apikey_exists)}','',f'Listen on IPv6 On: {YN_to_TF(env_listen_ipv6)}', sep='\t')
    print(f'Skip Pip Install On: {YN_to_TF(env_skip_pip)}',f'Skip Batch Install On: {YN_to_TF(env_skip_batch)}', sep='\t')
    blank_line()
    print(f'Model Selected: {C_text(env_default_model, "light_blue")}')
    if server_custom_models > 0:
        print(f'Included Models: {included_models}',f'Custom Models: {num_custom_models}', sep='\t')
    else:
        print(f'Included Models: {included_models}')
    blank_line()
    if port_check_result:
        print(f'1. {C_text("Start TTS Listening Server", "orange")}')
    else:
        print(S_text('1. '+ C_text("Start TTS Listening Server", "dark_grey")))
    print(f'2. {C_text("Run Initial Config Setup", "yellow")}')
    blank_line()
    print(f'X. {C_text("Exit", "red")}')
    blank_line()
    menu_option = input(f'{B_text("Enter Your Choice: ")} ')
    blank_line()
    if(menu_option == '1'):
        if port_check_result:
            print(f'{C_text("Starting TTS Listening Server...", "cyan")}')
            try: 
                start_serve()
            except Exception as e:
                print(f'{C_text(f"Error: {e}", "red")}')
                raise SystemExit('Exiting...')
        else:
            print(f'{C_text(f"Port {env_listen_port} is already in use!", "red")}')
            raise SystemExit('Exiting...')
    elif(menu_option == '2'):
        print(f'{C_text("Running Initial Config Setup...", "yellow")}')
        try:
            batch_builder(operating_system)
        except Exception as e:
            print(f'{C_text(f"Error: {e}", "red")}')
            raise SystemExit('Exiting...')
        
    elif(menu_option.lower() == 'x'):
        raise SystemExit('Exiting...')

if __name__ == "__main__":
    main()
