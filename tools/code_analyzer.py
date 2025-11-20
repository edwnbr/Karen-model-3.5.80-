import ast, os, json

def analyze_repo(root='.'):
    issues=[]
    for dirpath, dirs, files in os.walk(root):
        for fn in files:
            if fn.endswith('.py'):
                path=os.path.join(dirpath,fn)
                try:
                    with open(path,'r',encoding='utf-8') as f:
                        src=f.read()
                    tree=ast.parse(src)
                    for node in [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]:
                        # estimate function length using lineno attributes when present
                        start = getattr(node, 'lineno', None)
                        end = getattr(node, 'end_lineno', None)
                        if start and end and (end - start) > 120:
                            issues.append({'file':path,'issue':'long_function','function':node.name,'lines':end - start})
                    if 'TODO' in src or 'FIXME' in src:
                        issues.append({'file':path,'issue':'todo_found'})
                except Exception as e:
                    issues.append({'file':path,'issue':'parse_error','error':str(e)})
    return issues

def propose_fixes(issues):
    proposals=[]
    for it in issues:
        if it['issue']=='todo_found':
            proposals.append({'description':f"Remove TODOs in {it['file']}", 'patch':{}})
        if it['issue']=='long_function':
            proposals.append({'description':f"Refactor long function {it['function']} in {it['file']}", 'patch':{}})
    return proposals

if __name__=='__main__':
    iss=analyze_repo('.')
    print('Issues:', json.dumps(iss, indent=2, ensure_ascii=False))
    print('Proposals:', json.dumps(propose_fixes(iss), indent=2, ensure_ascii=False))
