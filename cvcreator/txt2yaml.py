"""Tool for migrating from old txt to new(er) yaml."""
import re
import yaml


def convert_txt_to_yaml(source: str, target: str) -> None:
    """Convert txt format to yaml."""
    data = {
        "Basic": {},
        "Summary": {},
        "Skills": {},
        "Languages": {},
        "SelectedSkills": {},
        "Education": [],
        "Work": [],
        "Interests": {},
        "Projects": {},
        "Publications": {},
    }

    cur = ""

    with open(source, "r") as f:
        text = f.read()

    text = re.sub(r"\n\\\> *", r"\n", text, 0, re.M)
    text = re.sub(r"([^\n]) *\\{2,} *\n", r"\1\n", text, 0, re.M)
    text = re.sub(r" +\n", r"\n", text, 0, re.M)
    text = re.sub(r" +$", r"", text)
    text = re.sub(r"\n{3,}", r"\n\n", text, re.M)

    groups = text.split("\n\n")

    for group in groups:

        header, _, content = group.partition("\n")

        if header == "Name:":
            data["Basic"]["Name"] = content

        elif header == "Address:":
            if "\n" in content:
                address, _, post = content.partition("\n")

                address = re.sub(r",$", "", address)

                data["Basic"]["Address"] = address
                data["Basic"]["Post"] = post

        elif header == "Birth:":
            data["Basic"]["Birth"] = content

        elif header == "Email:":
            data["Basic"]["Email"] = content

        elif header == "Phone:":
            data["Basic"]["Phone"] = content

        elif header == "Summary:":
            content = content.replace("\n", " ")
            data["Summary"] = content

        elif header == "Skills:":

            content = re.sub(r"([^\\]) *\& *", r"\1&", content)
            content = re.sub(r" *, *", r",", content)

            skills = content.split("\n")
            for skill in skills:
                title, _, listicle = skill.partition("&")
                data["Skills"][title] = listicle.split(",")

        elif header == "Languages:":

            content = re.sub(r" *\& *", r"&", content)
            content = content.split("\n")
            for c in content:
                c = c.split("&")
                data["Languages"][c[0]] = c[1]

        elif header == "SelectedSkills:":

            content = re.sub(r"([^\\]) *\& *", r"\1&", content)
            content = re.sub(r" *, *", r",", content)
            content = content.split("\n")
            for c in content:
                title, _, c = c.partition("&")
                data["SelectedSkills"][title] = c

        elif header == "Education:":

            content = re.sub(r"([^\\]) *\& *", r"\1&", content)
            content = content.split("\n")

            for c in content:
                p1, _, p2 = c.partition("&")
                data["Education"].append([p1, p2])

        elif header == "Work:":

            content = re.sub(r" *\& *", r"&", content)
            content = re.sub(r" *-- *", r"--", content)
            content = content.split("\n")

            for c in content:
                title, _, c = c.partition("&")
                if "--" in title:
                    t1, _, t2 = title.partition("--")
                    data["Work"].append([t1, t2, c])
                else:
                    data["Work"].append([title, c])

        elif header == "Interests:":

            content = re.sub(r" *\& *", r"&", content)
            content = re.sub(r" *, *", r",", content)

            skills = content.split("\n")
            for skill in skills:
                title, _, listicle = skill.partition("&")
                data["Interests"][title] = listicle.split(",")

        elif header[0] == "A":

            header = "A%d" % (int(header[1:-1])+1)
            data["Projects"][header] = a = {}

            for line in content.split("\n"):
                line = re.sub(r"^(\w+): +", r"\1:", line, 0, re.M)

                if line[:9] == "Activity:":
                    cur = "Activity"
                    a["Activity"] = line[9:]

                elif line[:5] == "Role:":
                    cur = "Role"
                    a["Role"] = line[5:]

                elif line[:9] == "Staffing:":
                    cur = "Staffing"
                    a["Staffing"] = line[9:]

                elif line[:12] == "Description:":
                    cur = "Description"
                    a["Description"] = line[12:]

                elif line[:6] == "Tools:":
                    cur = "Tools"
                    a["Tools"] = line[6:]
                else:
                    a[cur] += " " + line

        elif header[0] == "B":

            header = "B%d" % (int(header[1:-1])+1)
            data["Publications"][header] = b = {}

            entries = ["Journal", "Date", "Authors", "Title", "Summary", "DOI"]
            for entry in entries:
                if line.startswith(entry):
                    cur = entry
                    b[entry] = line[len(entry):]
                    break
            else:
                a[cur] += " " + line

    txt = yaml.dump(data, default_flow_style=False)

    target = target or source.replace(".txt", ".yaml")
    with open(target, "w") as f:
        f.write(txt)
