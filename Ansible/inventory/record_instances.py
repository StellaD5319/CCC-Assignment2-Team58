def record_ip():
    with open("inventory/inventory_file.ini") as f:
        hosts_starts = False
        hosts = []

        for line in f.readlines():
            line = line.replace("\n", "")

            if hosts_starts:
                if line == "":
                    hosts_starts = False

            if hosts_starts:
                hosts.append(line)

            if line == "[instances]":
                hosts_starts = True

        # Update inventory file
        with open("inventory/inventory.ini", "a") as ini_file:
            print("", file=ini_file)
            print("[instances]", file = ini_file)
            print("{}".format(hosts[0]), file=ini_file)
            print("{}".format(hosts[1]), file=ini_file)
            print("{}".format(hosts[2]), file=ini_file)
            print("", file=ini_file)
            print("[database]", file=ini_file)
            print("{}".format(hosts[0]), file=ini_file)
            print("", file=ini_file)
            print("[webserver]", file=ini_file)
            print("{}".format(hosts[1]), file=ini_file)
            print("", file=ini_file)
            print("[crawler]", file=ini_file)
            print("{}".format(hosts[2]), file=ini_file)
            print("", file=ini_file)

            # Update host variables file
            with open("host_vars/config.yaml", "a") as var_file:
                print("", file=var_file)
                print("database_ip: " + "{}".format(hosts[0]), file = var_file)
                print("", file=var_file)
                print("database_port: " + "{}".format(hosts[0]) + ":5000", file = var_file)

    return



if __name__ == "__main__":
    record_ip()


