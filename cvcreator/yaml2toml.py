"""Tool for migrating from old yaml to new one."""
import sys
import yaml
import toml


def main():
    """Convert from old to new yaml format."""
    if len(sys.argv) < 2:
        sys.exit(1)

    with open(sys.argv[1]) as src:
        content = yaml.safe_load(src)

    with open(sys.argv[2], "w") as dst:
        for name in content["Basic"]:
            toml.dump({name.lower(): content["Basic"][name]}, dst)

        toml.dump({"summary": content["Summary"].strip()}, dst)
        dst.write("\n")

        toml.dump({"technical_skill": [dict(title=title, values=values)
                                       for title, values in content.get("Skills", {}).items()]}, dst)
        toml.dump({"language_skill": [dict(language=language, proficiency=proficiency)
                                      for language, proficiency in content.get("Languages", {}).items()]}, dst)
        toml.dump({"personal_skill": [dict(title=title, description=description.strip())
                                      for title, description in content.get("SelectedSkills", {}).items()]}, dst)
        toml.dump({"hobby": [dict(title=title, values=values)
                             for title, values in content.get("Interests", {}).items()]}, dst)
        toml.dump({"education": [dict(year=year[-1], description=description.strip())
                                 for *year, description in content.get("Education", {})]}, dst)
        toml.dump({"work": [
            (dict(description=description.strip(), start=period[0]) if len(period) == 1 or not period[1] else
             dict(description=description.strip(), start=period[0], end=period[1]))
                                 for *period, description in content.get("Work", {})]}, dst)

        out = []
        for tag, project in content.get("Projects", {}).items():
            out.append({key.lower(): val for key, val in project.items()})
            out[-1]["tag"] = tag[1:]
        toml.dump({"project": out}, dst)

        out = []
        for tag, project in content.get("Publications", {}).items():
            out.append({key.lower(): val for key, val in project.items()})
            out[-1]["tag"] = tag[1:]
            out[-1]["year"] = out[-1].pop("date")
        toml.dump({"publication": out}, dst)
