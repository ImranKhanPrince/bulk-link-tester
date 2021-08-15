import re
import requests
import concurrent.futures
import winsound

def get_link(filename="links_with_other_words.txt"):
  pattern = r"((http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?)"

  with open(filename,'r',encoding="utf-8",) as f:
    buffer = f.read()
  jumbled_text= buffer.replace("\n", " ")
  url_list = re.findall(pattern, jumbled_text)

  return url_list

def send_request(url):
  print("Loading..... Please Wait!")
  try:
    status = requests.request("GET", url[0], timeout=2).status_code
  except:
    status = 404
  return (url[0], status)

def main():
  # get a link array from get_link
  filename = input("Enter the filename with extension: ")
  if(filename != "" and len(filename.split("."))>=1 and not (filename.split(".")[1] =="txt")):
    filename = filename + ".txt"
    url_list  = get_link(filename)
  else :
    url_list = get_link()

  # iterate those links to check the condition
  # store the data to somewhere 
  with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
    result = list(executor.map(send_request, url_list))

  html_basic ="""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>List of Links</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            ol {
                margin: 1rem;
                padding: 1rem;
                width: 100%;
            }
            ol li {
                border: 2px solid black;
                border-radius: 10px;
                margin: 2rem 4rem;
                padding: 1rem;
                text-align: center;
                font-size: 1.75rem;
                cursor: pointer;
            }
            li::marker {
                color: black;
            }
            li a {
                text-decoration: none;
                color: inherit;
                overflow: hidden;
                padding: 2rem 5rem;
            }
            .success {
                background: #42a148;
                color: white;
            }
            .success:hover {
                background: #3cfc49;
                color: black;
                transition: 0.5s ease;
            }
            .redirected {
                background: #c7cc00;
                color: black;
            }
            .redirected:hover {
                background: #fffb00;
                transition: 0.5s ease;
            }
            .failed {
                background: #ff7961;
                color: white;
                cursor: not-allowed;
            }
            .failed a {
                cursor: not-allowed;
            }
        </style>
</head>
<body>
  <ol>
   <!-- this is line 66 it'll change when you add css look at line 56 for context -->
  </ol>
</body>
</html>""".split("\n")

  # make an html file that shows active and inactive link
  with open("files.html","w+",encoding="utf-8") as f:
    for x in result:
      insert_element = f'<li class="{"success" if x[1]==200 else "redirected" if x[1]==403 else "failed" }"> {x[1]}-><a  href="{x[0]}" target="_blank">{x[0]}</a> </li>'
      html_basic.insert(65,insert_element)
    file_content = "".join(html_basic)
    f.write(str(file_content))

  winsound.Beep(1000,1000)

if __name__ == "__main__":
  main()