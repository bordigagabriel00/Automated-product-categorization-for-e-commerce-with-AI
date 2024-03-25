class ConfigProvider:
    def __init__(self):
        self.config = {}

    def set_config(self, section, attribute, value):
        if section not in self.config:
            self.config[section] = {}
        self.config[section][attribute] = value

    def get_config(self, section, attribute):
        return self.config.get(section, {}).get(attribute, None)

    def remove_config(self, section, attribute=None):
        if property and section in self.config:
            if property in self.config[section]:
                del self.config[section][attribute]
                if not self.config[section]:  # Si la sección está vacía, eliminarla
                    del self.config[section]
        elif section in self.config:
            del self.config[section]

    def show_configs(self):
        for section, attributes in self.config.items():
            print(f"Section: {section}")
            for attribute, value in attributes.items():
                print(f"  Property: {attribute}, Value: {value}")
