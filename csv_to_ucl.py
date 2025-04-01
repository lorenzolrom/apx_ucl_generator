import csv
import xml.etree.ElementTree as ET
import argparse
from xml.dom import minidom


def truncate_display_name(display_name):
    # Truncate the display name to 14 characters
    return display_name[:14]


def create_reference_key(system_name, unit_id, system_type):
    # ReferenceKey for ASTRO Conventional IDs: "1-" + unit_id + "-Individual"
    if system_type == 'Conventional':
        return f"1-{unit_id}-Individual"
    # ReferenceKey for ASTRO Trunking IDs: "1-1-" + unit_id
    elif system_type == 'Trunking':
        return f"1-1-{unit_id}"
    return ""


def create_xml_node(contact_name, system_name, unit_id, system_type):
    # Create a node for each contact
    node = ET.Element("Node", Name="Contacts", ReferenceKey=contact_name)

    # General section with Contact Name
    general_section = ET.SubElement(node, "Section", Name="General", id="10400")
    ET.SubElement(general_section, "Field", Name="Contact Name").text = contact_name

    # Add ASTRO 25 Trunking ID section - populated only for "Trunking"
    astro_trunking_section = ET.SubElement(node, "Section", Name="ASTRO 25 Trunking ID", id="10401", Embedded="True")
    embedded_recset = ET.SubElement(astro_trunking_section, "EmbeddedRecset", Name="ASTRO 25 Trunking ID List",
                                    Id="2201")

    if system_type == 'Trunking':
        reference_key = create_reference_key(system_name, unit_id, 'Trunking')
        embedded_node = ET.SubElement(embedded_recset, "EmbeddedNode", Name="ASTRO 25 Trunking ID",
                                      ReferenceKey=reference_key)
        embedded_section = ET.SubElement(embedded_node, "EmbeddedSection", Name="ASTRO 25 Trunking IDs", id="10402")
        ET.SubElement(embedded_section, "Field", Name="System Name").text = system_name
        ET.SubElement(embedded_section, "Field", Name="Custom WACN ID").text = "1"
        ET.SubElement(embedded_section, "Field", Name="Custom System ID").text = "1"
        ET.SubElement(embedded_section, "Field", Name="Unit ID").text = str(unit_id)
    else:
        # Do not add anything to ASTRO 25 Trunking ID if system_type is not "Trunking"
        pass

    # Add ASTRO Conventional ID section - Always included, even when empty
    astro_conventional_section = ET.SubElement(node, "Section", Name="ASTRO Conventional ID", id="10403",
                                               Embedded="True")
    embedded_recset = ET.SubElement(astro_conventional_section, "EmbeddedRecset", Name="Astro Conventional ID List",
                                    Id="2202")

    if system_type == 'Conventional':
        reference_key = create_reference_key(system_name, unit_id, 'Conventional')
        embedded_node = ET.SubElement(embedded_recset, "EmbeddedNode", Name="Astro Conventional ID",
                                      ReferenceKey=reference_key)
        embedded_section = ET.SubElement(embedded_node, "EmbeddedSection", Name="Astro Conventional IDs", id="10404")
        ET.SubElement(embedded_section, "Field", Name="System Name").text = system_name
        ET.SubElement(embedded_section, "Field", Name="Custom Group Number").text = "1"
        ET.SubElement(embedded_section, "Field", Name="Individual ID").text = str(unit_id)
        ET.SubElement(embedded_section, "Field", Name="Call Type").text = "Individual"
    else:
        # Do not add anything to ASTRO Conventional ID if system_type is not "Conventional"
        pass

    # Adding other sections with empty EmbeddedRecset elements
    # Type II Trunking ID section
    type_ii_section = ET.SubElement(node, "Section", Name="Type II Trunking ID", id="10411", Embedded="True")
    ET.SubElement(type_ii_section, "EmbeddedRecset", Name="Type II Trunking ID List", Id="2206")

    # MDC Conventional ID section
    mdc_conventional_section = ET.SubElement(node, "Section", Name="MDC Conventional ID", id="10405", Embedded="True")
    ET.SubElement(mdc_conventional_section, "EmbeddedRecset", Name="MDC Conventional ID List", Id="2203")

    # Phone Number section
    phone_number_section = ET.SubElement(node, "Section", Name="Phone Number", id="10413", Embedded="True")
    ET.SubElement(phone_number_section, "EmbeddedRecset", Name="Phone Number List", Id="2207")

    return node


def process_csv(input_file):
    contacts = []
    with open(input_file, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            contact_name = truncate_display_name(row['display_name'])
            system_name = row['system_name']
            unit_id = row['unit_id']
            system_type = row['system_type']
            contact_node = create_xml_node(contact_name, system_name, unit_id, system_type)
            contacts.append(contact_node)
    return contacts


def create_xml(contacts, output_file):
    # Create the root XML structure
    root = ET.Element("import_export_doc")

    # Version and Language moved outside the Root element
    version = ET.SubElement(root, "Version")
    version.text = "2"
    language = ET.SubElement(root, "Language")
    language.text = "en"

    # Adding the required Root element with attributes
    root_element = ET.SubElement(root, "Root", ExportedAllFeatures="False", ConverterGenerated="False")

    recset = ET.SubElement(root_element, "Recset", Name="Unified Call List", Id="2200")

    # Add the nodes for each contact
    for contact_node in contacts:
        recset.append(contact_node)

    # Generate the XML string with the encoding declaration
    xml_str = ET.tostring(root, encoding="UTF-8", xml_declaration=True).decode()

    # Pretty-print the XML
    pretty_xml_str = minidom.parseString(xml_str).toprettyxml(indent="  ")

    # Write the pretty XML to the output file
    with open(output_file, "w", encoding="UTF-8") as f:
        f.write(pretty_xml_str)


def main():
    parser = argparse.ArgumentParser(
        description="Convert a CSV of P25 Unit IDs and display names to Motorola APX CPS UCL XML format.")
    parser.add_argument("input_file", help="Input CSV file")
    parser.add_argument("output_file", help="Output XML file")

    args = parser.parse_args()

    contacts = process_csv(args.input_file)
    create_xml(contacts, args.output_file)
    print(f"Conversion completed. Output saved to {args.output_file}")


if __name__ == "__main__":
    main()
