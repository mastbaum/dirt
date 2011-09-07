def execute():
    '''reads a file and sends it as an attachment'''
    import os
    results = {'success': True, 'attachments': []}
    try:
        with open('/etc/hosts') as f:
            file_attachment = {'filename': os.path.basename(f.name), 'contents': f.read(), 'link_name': 'Hosts file'}
            results['attachments'].append(file_attachment)
    except Exception:
        results['success'] = False

    return results

if __name__ == '__channelexec__':
    results = execute()
    channel.send(results)

if __name__ == '__main__':
    print execute()
    
