# # Project Files and Directory Structures
# project_structures = {
#     "Node.js":{"files": ["package.json",".eslintrc.json",".prettierrc.json",".editorconfig"],
#                 "directories": ["node_modules","src","tests","db","scripts","logs","docs","assets"]}
#     ,
#     "Django":{"files": ["manage.py","requirements.txt"],
#                 "directories": ["myproject/","static/","media/","templates/","apps/","config/","logs/","migrations/","tests/"]}
#     ,
#     "Flask":{"files": ["app.py","main.py","requirements.txt","config.py"],
#                 "directories": ["static/","templates/","app/","tests/","instance/"]}
#     ,
#     "Laravel":{"files": ["artisan","composer.json","phpunit.xml","webpack.mix.js"],
#                 "directories": ["app/","bootstrap/","config/","database/","public/","resources/","routes/","storage/","tests/","vendor/"]}
#     ,
#     "Flutter":{"files": ["pubspec.yaml","analysis_options.yaml"],
#                 "directories": ["android/","ios/","lib/","test/","assets/","build/","web/"]}
#     ,
# }


# # Function to identify a Project structure
# def identify_project(user_project_structure):
#     result = {}
#     # try:
#     if True:
#         for project in project_structures.keys():
#             probability = 0
#             matches = 0
#             total = len(project_structures[project]["files"])+len(project_structures[project]["directories"])
#             # total = len(user_project_structure["files"])+len(user_project_structure["directories"])
#             for fil in user_project_structure["files"]:
#                 if fil in project_structures[project]["files"]:
#                     matches+=1
#                     break
#             for dire in user_project_structure["directories"]:
#                 if dire in project_structures[project]["directories"]:
#                     matches+=1
#                     break
#             probability=(matches/total)*100
#             if probability>0:
#                 result[project]=int(probability)
#         result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True)[:3]) if result else None
#     # except Exception as e:
#     #     result={"Error":e}
#     return result



identified_languages = []
# Identify programming language
languages = {
    'package.json': 'Node.js',
    'requirements.txt': 'Python',
    # 'gemfile': 'Ruby',
    # 'pom.xml': 'Java',
    # 'build.gradle': 'Groovy',
    # 'cargo.toml': 'Rust',
    'setup.py': 'Python',
    # 'composer.json': 'PHP',
    'dockerfile': 'Docker',
    # '.travis.yml': 'YAML',  # Travis CI configuration
    # '.gitlab-ci.yml': 'YAML',  # GitLab CI configuration
    # '.circleci/config.yml': 'YAML',  # CircleCI configuration
    # 'makefile': 'Makefile',
}

def get_supported_languages():
    return {"supported_languages":list(set(languages.values()))}

def identify_language(user_project_structure):
    result = {}
    try:
        for key in languages.keys():
            if key.lower() in  [ pfile.lower() for pfile in user_project_structure["files"]]:
                result={"language":languages[key],"main":key}
                break
    except Exception as e:
        result={}
    return result

# print(identify_project({"files":["package.json",".eslintrc.json",".prettierrc.json"],"directories": ["node_modules","src","tests"]}))