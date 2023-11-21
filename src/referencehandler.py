from converter import Converter
from reference import Reference
from reference_types import ReferenceTypes

class ReferenceHandler:
    def __init__(self, io):
        self.converter = Converter("example.json")
        self.io = io
        self.reference_types = ReferenceTypes("source_types.json")

    def info(self):
        self.io.write("Komennot: ")
        self.io.write("0 Sulje sovellus")
        self.io.write("1 Lisää kirja")
        self.io.write("2 Tulosta viitelista")


    def add(self):
        data = {}

        while True:
            input = self.io.read("\nLähteen avain: ('exit' peruaksesi toiminto) ")
            if input == "":
                self.io.write("\nKenttä ei voi olla tyhjä")
                continue
            if input == "exit":
                self.io.write("\nToiminto peruttu")
                return
            data["key"] = input
            break

        types = self.reference_types.get_types()

        self.io.write(f"\nMahdolliset lähdetyypit: {self._string_of_types(types)}")
        while True:
            input = self.io.read("\nLähteen tyyppi: ('exit' peruaksesi toiminto) ")
            if input == "":
                self.io.write("\nKenttä ei voi olla tyhjä")
                continue
            if input == "exit":
                self.io.write("\nToiminto peruttu")
                return
            if input not in types:
                self.io.write("\nTyyppi ei käytössä")
                continue
            data["type"] = input
            break
        
        data["fields"] = {}
        fields = self.reference_types.get_fields(data["type"])
        
        self.io.write("\nPakolliset kentät: ('exit' peruaksesi toiminto) ")
        for field in fields["required"]:
            while True:
                input = self.io.read(f"{field}: ")
                if input == "exit":
                    self.io.write("\nToiminto peruttu")
                    return
                if input == "":
                    self.io.write("\nKenttä ei voi olla tyhjä")
                    continue
                data["fields"][field] = input
                break

        self.io.write("\nVapaaehtoiset kentät: ('exit' peruaksesi toiminto, ENTER = seuraava kenttä) ")
        for field in fields["optional"]:
            while True:
                input = self.io.read(f"{field}: ")
                if input == "exit":
                    self.io.write("\nToiminto peruttu")
                    return
                if input == "":
                    break
                data["fields"][field] = input
                break

        new_reference = Reference(data)
        self.converter.add_reference(new_reference)
        self.io.write("\nLähde lisätty.")

    def list_references(self):
        self.io.write("Viitelista:")
        self.io.write(self.converter.convert())

    def run(self):
        self.info()
        while True:
            self.io.write("")
            command = self.io.read("Komento: ")
            if command == "0":
                break
            elif command == "1":
                self.add()
            elif command == "2":
                self.list_references()
            else:
                self.info()

    def _string_of_types(self, types):
        string = ""
        for type in types:
            string += type + " "
        return string