import sys, re

tokens = ["Name:", "Address:", "Birth:", "Email:", "Phone:", "Summary:", "Skills:", "Education:", "Work:", "Other:", "Interests:", "Languages:", "SelectedSkills:"]
subtokens = ["Activity:", "Role:", "Staffing:", "Description:", "Tools:"]

def extract_project(f):
   p = {}
   subt = ""
   line = f.next().strip()
   while (not line in tokens) and (not re.search("A\d\d?:", line)):
      new_token = False
      for s in subtokens:
         if s in line:
            subt = s
            new_token = True
            p[subt] = ""
      if subt:
         if new_token:
            p[subt] += line[len(subt):].lstrip()
         else:
            p[subt] += " " + line
      try:
         line = f.next().strip()
      except StopIteration:
         return p, line
   return p, line
 
def extract_cv(fn):
   of = open(fn, "r")
   content = {}
   
   token = of.readline().strip()
   
   try:
      while token:
         if token in tokens:
            line = ""
            content[token] = line
            while (not line in tokens) and (not re.search("A\d\d?:", line)):
               content[token] += line+"\n"
               line = of.next().strip()
            token = line
         elif (re.search("A\d\d?:", token)):
            old_token = token
            proj, token = extract_project(of)
            content[old_token] = proj
         else:
            token = of.next().strip()
   except StopIteration:
      pass
   return content

def generate_project(pdict, skipline=False):
   pstr = "\\begin{tabular}{@{}LR}\n"
   for token in subtokens:
      if token in pdict:
         pstr += token[:-1] + " & " + pdict[token] + "\\\\\n"
   if not skipline:
      pstr += """\\addlinespace \\bottomrule[.1pt] \\addlinespace
\\end{tabular}\n\n"""
   else:
      pstr += """\\end{tabular}\n\n"""
   return pstr

def generate_latex(namespace, projects):
   of = open("CV_mal.pytex", "r")
   cv_mal = of.read()
   of.close()
   for token in tokens:
      if token in namespace:
         cv_mal = re.sub("p"+token, namespace[token].replace('\\', '\\\\').strip(), cv_mal)

   project_content = ""
   for p in projects[:-1]:
      project_content += generate_project(namespace[p])

   project_content += generate_project(namespace[projects[-1]], skipline=True)

   cv_mal = re.sub("pProjects:", project_content.replace('\\', '\\\\').strip(), cv_mal)
   
   tf = open("GeneratedCV.tex", "w")
   tf.write(cv_mal)
   tf.write("\n")
   tf.close() 
   

if __name__ == "__main__":
   filename = sys.argv[1]
   projects = ["A%s:" % i for i in sys.argv[2:]]
   content = extract_cv(filename)
   generate_latex(content, projects)
