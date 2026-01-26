from main_classes.bing.downloader import download

def find_images(query: str, limit=1, output_dir="data/images/downloaded", verbose=False):
  return download(query, limit=limit, output_dir=output_dir, adult_filter_off=False, timeout=60, verbose=verbose)