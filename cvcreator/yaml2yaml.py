"""Tool for migrating from old yaml to new one."""
import sys
import yaml


def main():
    """Convert from old to new yaml format."""
    if len(sys.argv) < 2:
        sys.exit(1)

    with open(sys.argv[1]) as src:
        content = yaml.safe_load(src)

    with open(sys.argv[2], "w") as dst:
        for name in content["Basic"]:
            yaml.safe_dump({name.lower(): content["Basic"][name]}, dst, default_flow_style=False)

        yaml.safe_dump({"summary": content["Summary"].strip()}, dst, default_flow_style=False)

        yaml.safe_dump({"technical_skill": [dict(title=title, values=values)
                                            for title, values in content.get("Skills", {}).items()]},
                       dst, default_flow_style=False)

        yaml.safe_dump({"language_skill": [dict(language=language, proficiency=proficiency)
                                           for language, proficiency in content.get("Languages", {}).items()]},
                       dst, default_flow_style=False)

        yaml.safe_dump({"personal_skill": [dict(title=title, description=description.strip())
                                           for title, description in content.get("SelectedSkills", {}).items()]},
                       dst, default_flow_style=False)

        yaml.safe_dump({"hobby": [dict(title=title, values=values)
                                  for title, values in content.get("Interests", {}).items()]},
                       dst, default_flow_style=False)

        yaml.safe_dump({"education": [dict(year=year[-1], description=description.strip())
                                      for *year, description in content.get("Education", {})]},
                       dst, default_flow_style=False)

        yaml.safe_dump({"work": [dict(period=(list(period) if len(period) == 2 else [period[0], ""]),
                                      description=description.strip())
                                 for *period, description in content.get("Work", {})]},
                       dst, default_flow_style=False)

        out = []
        for tag, project in content.get("Projects", {}).items():
            out.append({key.lower(): val for key, val in project.items()})
            out[-1]["tag"] = tag[1:]
        yaml.safe_dump({"project": out}, dst, default_flow_style=False)

        out = []
        for tag, project in content.get("Publications", {}).items():
            out.append({key.lower(): val for key, val in project.items()})
            out[-1]["tag"] = tag[1:]
        yaml.safe_dump({"publication": out}, dst, default_flow_style=False)
