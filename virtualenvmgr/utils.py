
# print table #
def pptable(table):             
    head = table['head']
    body = table['body']
    pretty_head = [
                '+' + '+'.join(['{:->24}'.format('') for n in head]) + '+',
                '|' + '|'.join(['{:^24}'.format(str(n)[-24:]) for n in head]) + '|',
                '+' + '+'.join(['{:=>24}'.format('') for n in head]) + '+',
        ]
    pretty_body = []
    for row in body:
        pretty_body.append(
                    '|' + '|'.join(['{:>24}'.format(str(n)[-24:]) for n in row]) + '|',
                )
        pretty_body.append(
                    '+' + '+'.join(['{:->24}'.format('') for n in head]) + '+',
                )
    prettytable = '\n'.join(
            pretty_head + pretty_body
        )
    print(prettytable)