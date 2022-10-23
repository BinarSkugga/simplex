# simplex
Simple Python IDL

Heres what simple_class.simp will generate:

```
{
  CLASS(Test): {'fields': [], 'index': 1, 'parent': None},
  CLASS(Roger): {'fields': [
                              [type(int), FIELD(age), =, VALUE(67)]
                           ],
                'index': 5,
                'parent': type(Test)
  },
  CLASS(Blop): {'fields': [
                              [type(int), FIELD(id), =, VALUE(3)]
                          ],
               'index': 22,
               'parent': type(BaseModel)
  },
  CLASS(Zone): {'fields': [
                              [type(Blop), FIELD(test)],
                              [type(str), FIELD(name), =, VALUE(#\"Charles Smith)]
                          ],
               'index': 34,
               'parent': type(Roger)
  },
  CLASS(BaseModel): {'fields': [], 'index': 18, 'parent': None}}
```
