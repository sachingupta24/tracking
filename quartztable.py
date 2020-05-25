from flask_table import Table, Col, LinkCol


class Results(Table):
    id = Col('Id', show=False)
    title = Col('Title')
    quartzserialnumber = Col('QuartzSerialNumber')
    quartz_type = Col('QuartzType')
    installation_date = Col('Installation Date')
    toolname = Col('ToolName')
    edit = LinkCol('Edit', 'edit', url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete', url_kwargs=dict(id='id'))