s = """domain1.icu
domain2.icu
domain3.icu
domain4.cyou
domain5.cyou
domain6.cyou
domain7.cyou
domain8.cyou
domain9.sbs
domain10.sbs"""  # Replace these with the actual obtained SUBJECT_ALTERNATIVE_NAME

tld_dict = {}
for line in s.split('\n'):
    domain = line.strip()
    sld, tld = domain.rsplit('.', maxsplit=1)

    if tld in tld_dict:
        tld_dict[tld] += 1
    else:
        tld_dict[tld] = 1

print(tld_dict)
print(sum(tld_dict.values()))
