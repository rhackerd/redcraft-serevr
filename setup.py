import questionary

def asks(versions):
    server_name = questionary.text('Server name:', default='my-server').ask()
    port = questionary.text('Port:', default='25566').ask()
    motd = questionary.text('MOTD:').ask()
    max_players = questionary.text("Max players:", default="20").ask()
    _ip = questionary.text("IP", default="localhost").ask()
    ip = "localhost"
    if _ip != "localhost":
        if questionary.confirm("in old redcraft versions doesn't support anything than localhost, are u sure ?").ask():
            if questionary.confirm("Are u really sure ? (double confim)").ask():
                ip = _ip
            else:
                ip = "localhost"
        else:
            ip = "localhost"
    game_versions = questionary.select("Joinable version", versions).ask()
    
    return server_name, port, motd, max_players, ip, game_versions

def show_answers(server_name, port, motd, max_players, ip, game_versions):
    
    questionary.print(f"Server name: {server_name}", style="bold fg:white")
    print(f"Port: {port}")
    print(f"MOTD: {motd}")
    print(f"Max players: {max_players}")
    print(f"IP: {ip}")
    print(f"Game versions: {game_versions}")
    
    
def save_config(file_path, server_name, port, motd, max_players, ip, game_versions):
    with open(file_path, 'w') as f:
        f.write(f"PORT = {port}\n")
        f.write(f"IP = \"{ip}\"\n")
        f.write(f"MOTD = \"{motd}\"\n")
        f.write(f"MAX_PLAYERS = {max_players}\n")
        f.write(f"MAX_PLAYERS_PER_IP = 1\n")
        f.write(f"MAX_PLAYERS_PER_NAME = 1\n")
        f.write(f"MAX_PLAYERS_PER_UUID = 1\n")
        f.write(f"MAX_PACKETS_PER_TICK = 20\n")
        f.write(f"SERVER_NAME = \"{server_name}\"\n")
        f.write(f"SERVER_VERSION = '1.0.0'\n")
        f.write(f"GAME_VERSION = '{game_versions}'\n")

if __name__ == "__main__":
    versions = [
        "0.6.8"
    ] # "generation.versions.beta"
    # so for example 1.2 is full versions and 1.2.6 is just testing version
    # and other versions like 0.5 were like the pygame testing and choosing right engine
    server_name, port, motd, max_players, ip, game_versions = asks(versions)
    show_answers(server_name, port, motd, max_players, ip, game_versions)
    while not questionary.confirm("Are you sure with this config ?").ask():
        server_name, port, motd, max_players, ip, game_versions = asks(versions)
        show_answers(server_name, port, motd, max_players, ip, game_versions) 
        
    save_config('settings.py', server_name, port, motd, max_players, ip, game_versions)
    print(f"Configuration saved to 'server_config.env'")
    print("to launch server run 'python main.py'")