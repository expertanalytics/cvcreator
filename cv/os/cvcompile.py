#!/usr/bin/env python

"""
Copyright (c) 2013 Expert Analytics AS.
All rights reserved.

Redistribution and use in source and binary forms are permitted
provided that the above copyright notice and this paragraph are
duplicated in all such forms and that any documentation,
advertising materials, and other materials related to such
distribution and use acknowledge that the software was developed
by Expert Analytics AS.  The name of Expert Analytics AS
may not be used to endorse or promote products derived
from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED ``AS IS'' AND WITHOUT ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
"""

import re

class CVGenerator(object):
   """Based on a latex template and a user defined content file, generate the xal CV in latex"""

   def __init__(self, filename, outfilename, projects):
      self.filename = filename
      self.outfilename = outfilename
      self.projects = projects

      # Sections of the CV
      self._mandatory_tokens = ["Name:", "Address:", "Birth:", "Email:", "Phone:", "Summary:"]
      # Optional sections, in given order
      self._optional_tokens = ["Skills:", "Education:", "Work:", "Other:", "Languages:", "SelectedSkills:", "Interests:"]
      # Sections in the project descriptions
      self._project_tokens = ["Activity:", "Role:", "Staffing:", "Description:", "Tools:"]
      # Hard coded template file for now
      self.templatefile =  "CV_mal.pytex"

   def mandatory_tokens(self):
      for token in self._mandatory_tokens:
         yield token

   def optional_tokens(self):
      for token in self._optional_tokens:
         yield token

   def tokens(self):
      for token in self.mandatory_tokens():
         yield token
      for token in self.optional_tokens():
         yield token

   def project_tokens(self):
      for token in self._project_tokens:
         yield token

   def extract_project(self, f):
      p = {}
      subt = ""
      line = f.next().strip()
      while (not line in self.tokens()) and (not re.search("A\d\d?:", line)):
         new_token = False
         for s in self.project_tokens():
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
    
   def extract_cv(self):
      of = open(self.filename, "r")
      content = {}
   
      match = None
      if len(self.projects) == 0:
         c = of.read()
         of.seek(0)
         self.projects = re.findall("^A\d\d?:", c, flags=re.M)
      
      token = of.readline().strip()
   
      try:
         while token:
            if token in self.tokens():
               line = ""
               content[token] = line
               while (not line in self.tokens()) and (not re.search("A\d\d?:", line)):
                  content[token] += line+"\n"
                  line = of.next().strip()
               token = line
            elif (re.search("A\d\d?:", token)):
               old_token = token
               proj, token = self.extract_project(of)
               content[old_token] = proj
            else:
               token = of.next().strip()
      except StopIteration:
         pass
      return content
   
   def generate_project(self, pdict, skipline=False):
      pstr = "\\begin{tabular}{@{}LR}\n"
      for token in self.project_tokens():
         if token in pdict:
            pstr += token[:-1] + " & " + pdict[token] + "\n"
      if not skipline:
         pstr += """\\addlinespace \\bottomrule[.1pt] \\addlinespace
   \\end{tabular}\n\n"""
      else:
         pstr += """\\end{tabular}\n\n"""
      return pstr
   
   def generate_latex(self, namespace):
      of = open(self.templatefile, "r")
      cv_mal = of.read()
      of.close()
      templates = {}
      exec(cv_mal, templates)
      cv_mal = templates["header_template"]
      for token in self.mandatory_tokens():
         if token in namespace:
            cv_mal = re.sub("p"+token, namespace[token].replace('\\', '\\\\').strip(), cv_mal)
   
      cv_mal += "\n"
   
      for token in self.optional_tokens():
         if token in namespace:
            text = templates[token[:-1]+"_template"]
            text = re.sub("p"+token, namespace[token].replace('\\', '\\\\').strip(), text)
            cv_mal += text + "\n"
   
      project_content = ""
      for p in self.projects[:-1]:
         project_content += self.generate_project(namespace[p])
   
      project_content += self.generate_project(namespace[self.projects[-1]], skipline=True)
   
      text = templates["footer_template"]
      text = re.sub("pProjects:", project_content.replace('\\', '\\\\').strip(), text)
      cv_mal += text
      
      tf = open(self.outfilename, "w")
      tf.write(cv_mal)
      tf.write("\n")
      tf.close() 

def usage():
   import sys
   print r"""XAL CV Generator usage:
%s -i content [-o texfile] [i1 i2 i3 i4 ...]
%s --input content [--output texfile] [i1 i2 i3 i4 ...]

content: file containing the cv content
textfile: name of generated tex file, defaults to "GeneratedCV.tex"
i1, etc.: extended project descriptions in content file to include. Defaults to all.""" % (sys.argv[0], sys.argv[0])
   
if __name__ == "__main__":
   import sys, getopt 
   try:
      opts, args = getopt.getopt(sys.argv[1:], "i:o:", ["input=", "output="])
   except getopt.GetoptError as err:
      print str(err)
      usage()
      sys.exit(2)

   filename = None
   outfilename = "GeneratedCV.tex"

   for o,a in opts:
      if o in ["-i", "--input"]:
         filename = a
      elif o in ["-o", "--output"]:
         outfilename = a

   if filename is None:
      usage()
      sys.exit(2)

   generator = CVGenerator(filename, outfilename, ["A%s:" % i for i in args])
   content = generator.extract_cv()
   generator.generate_latex(content)
