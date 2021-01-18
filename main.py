from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
import time
import sqlite3
import numpy as np
import pickle


PATH = "C:\Program Files (x86)\chromedriver.exe"
platforms = ["ABAP", "AGS Script", "AMPL", "ANTLR", "API Blueprint", "ASP.NET", "ActionScript", "Ada", "AngelScript", "ApacheConf", "Apex", "AppleScript", "AspectJ", "Assembly", "AutoHotkey", "Awk", "Batchfile", "BitBake", "Blade", "BlitzBasic", "C", "C#", "CMake", "COBOL", "CSS", "CartoCSS", "Classic ASP", "Clojure", "CodeQL", "CoffeeScript", "Common Lisp", "Coq", "Crystal", "Cuda", "D", "DIGITAL Command Language", "DTrace", "Dart", "Dhall", "Dockerfile", "Dogescript", "ECL", "Elixir", "Elm", "Emacs Lisp", "Erlang", "F#", "FLUX", "Forth", "Fortran", "FreeMarker", "GAP", "GCC Machine Description", "GDB", "GDScript", "GLSL", "Game Maker Language", "Gherkin", "Gnuplot", "Go", "Groovy", "HCL", "HLSL", "HTML", "Hack", "Haml", "Handlebars", "Harbour", "Haskell", "Haxe", "HiveQL", "HolyC", "Hy", "IDL", "Inno Setup", "JSONiq", "Jasmin", "Java", "JavaScript", "Jsonnet", "Julia", "Jupyter Notebook", "Kaitai Struct", "Kotlin", "LLVM", "Less", "Lex", "Liquid", "LiveScript", "Logos", "Lua", "M4", "MATLAB", "MLIR", "Makefile", "Mako", "Markdown", "Marko", "Mathematica", "Max", "Meson", "Metal", "NASL", "NSIS", "Nearley", "NewLisp", "Nginx", "Nim", "Nix", "OCaml", "Objective-C", "Objective-J", "OpenEdge ABL", "Other", "Oz", "PHP", "PLSQL", "PLpgSQL", "Parrot", "Pascal", "Perl", "PigLatin", "Pony", "PostScript", "PowerShell", "Processing", "Prolog", "Protocol Buffer", "Pug", "Puppet", "PureBasic", "PureScript", "Python", "QML", "QMake", "R", "RAML", "REXX", "Racket", "Ragel", "Raku", "ReScript", "Reason", "Rebol", "RenderScript", "Rich Text Format", "Riot", "RobotFramework", "Roff", "Ruby", "Rust", "SCSS", "SMT", "SQLPL", "SRecode Template", "SWIG", "Sage", "SaltStack", "Sass", "Scala", "Scheme", "Scilab", "ShaderLab", "Shell", "Slim", "Smali", "Smalltalk", "Smarty", "Solidity", "SourcePawn", "Squirrel", "Stan", "Standard ML", "Starlark", "Stylus", "SuperCollider", "Svelte", "Swift", "TLA", "TSQL", "Tcl", "TeX", "Terra", "Thrift", "Twig", "TypeScript", "V", "VBA", "VBScript", "VCL", "VHDL", "Vala", "Verilog", "Vim Snippet", "Vim script", "Visual Basic .NET", "Volt", "Vue", "Web Ontology Language", "WebAssembly", "WebIDL", "XC", "XML", "XQuery", "XS", "XSLT", "Xtend", "YASnippet", "Yacc", "sed", "xBase"]
conn = sqlite3.connect("repositoryurls_db.db")
curr = conn.cursor()
curr.execute(
	"""create table if not exists repositorydurls_tb (
	link text
	)""")

curr.execute(
	"""create table if not exists crawledlangs_tb (
	langs text
	)""")


    
    
def store_db(link):
    curr.execute("insert into repositoryurls_tb values (?)", (link,))
    conn.commit()

def store_l_db(lang):
    curr.execute("insert into crawledlangs_tb values (?)", (lang,))
    conn.commit()

def get_db():
    curr.execute('SELECT * FROM repositoryurls_tb')
    result = curr.fetchall()
    result = np.asarray(result).flatten().tolist()
    return result

def get_l_db():
    curr.execute('SELECT * FROM crawledlangs_tb')
    result = curr.fetchall()
    result = np.asarray(result).flatten().tolist()
    return result


def scrape():
    did = get_l_db()
    count = 1
    countM = len(platforms)
    for p in platforms:
        try:
            print(str(count)+"   of   "+str(countM))
            count+=1
            if p not in did or count == 161:
                driver = webdriver.Chrome(PATH)
                driver.get("https://github.com/topics/{}".format(p))

                while True:
                    try:
                        btn = WebDriverWait(driver, 10).until(
                                        EC.presence_of_element_located((By.CLASS_NAME, "mt-0.width-full"))
                                )
                        btn.click()
                        print("               clicked            ")
                        time.sleep(2)

                    except Exception as e:
                        data = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.CLASS_NAME, "col-lg-9"))
                        )
                        content = data.find_elements_by_class_name("my-4")
                        fin = get_db()
                        fin = np.unique(np.asarray(fin))
                        for c in content:
                                if c not in fin:
                                        des = c.find_element_by_class_name("text-bold")
                                        links = des.get_attribute("href")
                                        store_db(links)
                                        length = len(fin)
                        print("                    fetched:   " + str(length)+"from "+p)

                        print("exceptions:             ")
                        print(str(len(fin))+"/"+str(len(get_db())))
                        print(e)
                        break
                    
                store_l_db(p)

            else:
                    print("already crawled")
        except Exception as e:
            print(e)
    print("                   finalised                  ")
    #driver.quit()


if __name__ == "__main__":
    scrape()




