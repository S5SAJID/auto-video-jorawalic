def get_plain_script(segments):
  script = ""
  for i, sg in enumerate(segments):
    script += " ".join(sg['words']) + ", "
  return script

