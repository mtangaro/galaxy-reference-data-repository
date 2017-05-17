'''
comments here
'''

import os
import argparse
import yaml
import urllib2
import logging
import pycurl

GALAXY_USER='galaxy'
LOG_FILENAME = "/tmp/refdata_download.log"

def parse_cli_options():
  parser = argparse.ArgumentParser(description='Download Reference Data', formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument( '-i', '--input',  dest='genome_list', help='')
  parser.add_argument( '-o', '--outdir', default='/refdata', dest='outdir', help='')
  parser.add_argument( '-s', '--space', default='elixir-italy.galaxy.refdata', dest='space', help='')
  return parser.parse_args()

def load_input_file(refdata_list_file = "genome-list.yml"):
  with open(refdata_list_file, 'r') as fi:
    li = yaml.load(fi)
  return li

def clear_log(log):
  with open(log, 'w'):
    pass

def create_dir(dirpath = 'directory_path'):
  if not os.path.exists(dirpath):
    os.makedirs(dirpath)

def write_data(name, url):
  out = 'Downloading: ' + url
  logging.debug(out)
  try: 
    response = urllib2.urlopen(url)
    with open(name, "wb") as fp:
      curl = pycurl.Curl()
      curl.setopt(pycurl.URL, url)
      curl.setopt(pycurl.WRITEDATA, fp)
      curl.perform()
      curl.close()
      fp.close()
  except (urllib2.HTTPError):
    logging.debug('WARNING: Reference Genome NOT FOUND. SKIPPING!!!')
    pass

def download():
  options = parse_cli_options()
  li = load_input_file(options.genome_list)

  clear_log(LOG_FILENAME)
  logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
  logging.debug('>>> Reference Data download log file.')

  #print li
  outdir=options.outdir + '/' + options.space
  print outdir
  create_dir(outdir)
  recas_url='http://cloud.recas.ba.infn.it:8080/v1/AUTH_3b4918e0a982493e8c3ebcc43586a2a8/test_ref'
  
  for i in li['genomes']:
    genome_dir = outdir +'/'+i['genome']
    #print genome_dir
    create_dir(genome_dir)
    os.chdir(genome_dir)

    for j in i['others']:
      url_1 = recas_url + '/' + i['genome'] + '/' + j['other'] 
      #print url_1
      write_data(j['other'], url_1)

    for j in i['tools']:
      #os.chdir(genome_dir)
      tool_dir = genome_dir + '/' + j['tool']
      create_dir(tool_dir)

      for k in j['parts']:
        os.chdir(tool_dir)
        url_2 = recas_url+'/'+i['genome']+'/'+j['tool']+'/'+k['part']
        write_data(k['part'], url_2)

if __name__ == "__main__":
  download()
