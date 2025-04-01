
# CSV to Motorola APX CPS UCL XML Conversion Tool

This Python script converts a CSV file containing P25 Unit IDs and display names into a Motorola APX CPS Unified Call List (UCL) XML format.

## Requirements

### Python 3.x

Make sure Python 3.x is installed. You can verify this by running:

```bash
python --version
```

or

```bash
python3 --version
```

### Create a Virtual Environment

It is recommended to use a virtual environment for this project to manage dependencies. Here are the steps to set it up:

1. **Create a virtual environment**:

   ```bash
   python3 -m venv venv
   ```

2. **Activate the virtual environment**:

   - **For macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

   - **For Windows**:
     ```bash
     venv\Scriptsctivate
     ```

3. **Install dependencies**:

   Use the provided `requirements.txt` file to install the necessary dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## requirements.txt

Here is the content of `requirements.txt` that you should include in the project directory:

```
argparse
```

## CSV File Format

The input CSV file should have the following columns:

| Column Name   | Description                                      | Example                        |
| ------------- | ------------------------------------------------ | ---------------------------- |
| `system_type` | Type of the system, either `Trunking` or `Conventional` | Trunking                        |
| `system_name` | The name of the system                          | SKYNET                         |
| `unit_id`     | The P25 Unit ID                                 | 5002083                        |
| `display_name`| The display name of the contact (maximum 14 characters) | Lorenzo APX900                 |

### Example CSV File:
```csv
system_type,system_name,unit_id,display_name
Trunking,SKYNET,5002123,Larry APX
Conventional,TACTICAL,1012,Ron Wood XTL
```

## How to Run

1. Ensure you have Python 3.x installed and set up the virtual environment.
2. Save your CSV file.
3. Run the script from the command line using the following format:

### Command:
```bash
python csv_to_ucl.py input.csv output.xml
```

- `input.csv`: Path to your input CSV file.
- `output.xml`: Desired path for the output XML file.

### Example:
```bash
python csv_to_ucl.py contacts.csv ucl_output.xml
```

This will convert the `contacts.csv` file into the `ucl_output.xml` file in the correct Motorola APX CPS Unified Call List format.

## Output Format

The script generates an XML file where each contact is represented as a `<Node>` element. The **ASTRO 25 Trunking ID** and **ASTRO Conventional ID** sections are included based on the `system_type`. The order of sections is:

1. **Type II Trunking ID** (always included)
2. **ASTRO Conventional ID** (always included but empty if `system_type` is `Trunking`)
3. **MDC Conventional ID** (always included)
4. **Phone Number** (always included)

### Example of the Generated XML for Trunking:
```xml
<Node Name="Contacts" ReferenceKey="Lorenzo APX900">
  <Section Name="General" id="10400">
    <Field Name="Contact Name">Lorenzo APX900</Field>
  </Section>
  <Section Name="ASTRO 25 Trunking ID" id="10401" Embedded="True">
    <EmbeddedRecset Name="ASTRO 25 Trunking ID List" Id="2201">
      <EmbeddedNode Name="ASTRO 25 Trunking ID" ReferenceKey="1-1-5002083">
        <EmbeddedSection Name="ASTRO 25 Trunking IDs" id="10402">
          <Field Name="System Name">SKYNET</Field>
          <Field Name="Custom WACN ID">1</Field>
          <Field Name="Custom System ID">1</Field>
          <Field Name="Unit ID">5002083</Field>
        </EmbeddedSection>
      </EmbeddedNode>
    </EmbeddedRecset>
  </Section>
  <Section Name="ASTRO Conventional ID" id="10403" Embedded="True">
    <EmbeddedRecset Name="Astro Conventional ID List" Id="2202" />
  </Section>
  <Section Name="Type II Trunking ID" id="10411" Embedded="True">
    <EmbeddedRecset Name="Type II Trunking ID List" Id="2206" />
  </Section>
  <Section Name="MDC Conventional ID" id="10405" Embedded="True">
    <EmbeddedRecset Name="MDC Conventional ID List" Id="2203" />
  </Section>
  <Section Name="Phone Number" id="10413" Embedded="True">
    <EmbeddedRecset Name="Phone Number List" Id="2207" />
  </Section>
</Node>
```

### Example of the Generated XML for Conventional:
```xml
<Node Name="Contacts" ReferenceKey="Lorenzo APX900">
  <Section Name="General" id="10400">
    <Field Name="Contact Name">Lorenzo APX900</Field>
  </Section>
  <Section Name="ASTRO 25 Trunking ID" id="10401" Embedded="True">
    <EmbeddedRecset Name="ASTRO 25 Trunking ID List" Id="2201" />
  </Section>
  <Section Name="ASTRO Conventional ID" id="10403" Embedded="True">
    <EmbeddedRecset Name="Astro Conventional ID List" Id="2202">
      <EmbeddedNode Name="Astro Conventional ID" ReferenceKey="1-5002083-Individual">
        <EmbeddedSection Name="Astro Conventional IDs" id="10404">
          <Field Name="System Name">SKYNET</Field>
          <Field Name="Custom Group Number">1</Field>
          <Field Name="Individual ID">5002083</Field>
          <Field Name="Call Type">Individual</Field>
        </EmbeddedSection>
      </EmbeddedNode>
    </EmbeddedRecset>
  </Section>
  <Section Name="Type II Trunking ID" id="10411" Embedded="True">
    <EmbeddedRecset Name="Type II Trunking ID List" Id="2206" />
  </Section>
  <Section Name="MDC Conventional ID" id="10405" Embedded="True">
    <EmbeddedRecset Name="MDC Conventional ID List" Id="2203" />
  </Section>
  <Section Name="Phone Number" id="10413" Embedded="True">
    <EmbeddedRecset Name="Phone Number List" Id="2207" />
  </Section>
</Node>
```

## Notes

- The **ASTRO 25 Trunking ID** and **ASTRO Conventional ID** sections are included but may remain empty depending on the `system_type`. If `system_type` is `"Trunking"`, the **ASTRO Conventional ID** section is empty. If `system_type` is `"Conventional"`, the **ASTRO 25 Trunking ID** section is empty.
- All sections (`Type II Trunking ID`, `MDC Conventional ID`, `Phone Number`) are always present, but empty `EmbeddedRecset` elements are added when no data is provided.
