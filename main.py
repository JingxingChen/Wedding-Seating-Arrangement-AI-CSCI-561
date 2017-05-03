# from utils import unique


class WeddingSeatingPlanner():
    YES = 'yes'
    NO = 'no'
    all_clauses_list_list = []
    temp = str()
    subset_flag = True

    def __init__(self):
        self.enemy = False
        self.table_number = 1
        input_file = open("input.txt", 'r')
        line = input_file.readline()
        # line = ''.join(c for c in line if c not in '\n'' ')
        line = line.split()
        self.m = int(line[0])
        self.n = int(line[1])
        # print(self.m)
        # print(self.n)

        self.assign_table = {}  # Use to assign table to each person
        for i in range(self.m):
            self.assign_table[i + 1] = 0

        self.make_one_table_per_person_clauses()

        while True:
            line = input_file.readline()
            line = ''.join(c for c in line if c not in '\n'' ')
            if "" == line:
                break;
            # print(line[0] + line[1] + line[2])
            if line[2] == 'E':
                self.enemy = True
                self.make_enemy_clauses(line)
                # relationship_matrix[(int(line[0])) - 1][(int(line[1]) - 1)] = line[2]
            if line[2] == 'F':
                self.make_friend_clause(line)
        print(self.all_clauses_list_list)
        # print(len(self.all_clauses_list_list))

    def make_one_table_per_person_clauses(self):
        a = str()
        one_person_one_table_clause = []
        for i in range(self.m):
            for j in range(self.n):
                one_person_one_table_clause = []
                a = 'X' + str(i + 1) + str(j + 1)
                one_person_one_table_clause.append(a)
            self.all_clauses_list_list.append(one_person_one_table_clause)
        for i in range(self.m):
            for j in range(self.n):
                for k in range(j + 1, self.n):
                    one_person_one_table_clause = []
                    a = '~X' + str(i + 1) + str(j + 1)
                    one_person_one_table_clause.append(a)
                    a = '~X' + str(i + 1) + str(k + 1)
                    one_person_one_table_clause.append(a)
                    self.all_clauses_list_list.append(one_person_one_table_clause)

    def make_friend_clause(self, line):

        for i in range(self.n):
            friend_clauses = []
            self.temp = '~X' + str(line[0]) + str(i + 1)
            friend_clauses.append(self.temp)
            self.temp = 'X' + str(line[1]) + str(i + 1)
            friend_clauses.append(self.temp)
            self.all_clauses_list_list.append(friend_clauses)
            friend_clauses = []
            self.temp = 'X' + str(line[0]) + str(i + 1)
            friend_clauses.append(self.temp)
            self.temp = '~X' + str(line[1]) + str(i + 1)
            friend_clauses.append(self.temp)
            self.all_clauses_list_list.append(friend_clauses)

    def make_enemy_clauses(self, line):
        for i in range(self.n):
            enemy_clauses = []
            self.temp = '~X' + str(line[0]) + str(i + 1)
            enemy_clauses.append(self.temp)
            self.temp = '~X' + str(line[1]) + str(i + 1)
            enemy_clauses.append(self.temp)
            self.all_clauses_list_list.append(enemy_clauses)

    def populate_output(self, b):
        output_file = open("output.txt", "w")

        if b:
            output_file.write(self.YES)

            for key, value in self.assign_table.items():
                self.output = ("\n{0} {1}".format(key, value))
                output_file.write(self.output)
        else:
            output_file.write(self.NO)

        output_file.close()

    def pl_resolution(self):
        "Propositional-logic resolution: say if alpha follows from KB. [Figure 7.12]"
        clauses = self.all_clauses_list_list
        new = []
        while True:
            self.subset_flag = True
            n = len(clauses)
            pairs = [(clauses[i], clauses[j])
                     for i in range(n) for j in range(i + 1, n)]
            # print(pairs)
            for (ci, cj) in pairs:
                # print('yes')
                # print(ci)
                # print(cj)
                resolvents = self.pl_resolve(ci, cj)
                # print(resolvents)
                for element in resolvents:
                    # print('yes')
                    if not element:
                        return False
                for element in new:
                    if not resolvents.__contains__(element):
                        resolvents.append(element)
                # new = new.union(set(resolvents))
                new = resolvents
                # print('yahan')
                # print(resolvents)
                # print(new)

            for i in new:
                for k in clauses:
                    if not sorted(k) == sorted(i):
                        self.subset_flag = False
                        break

            if self.subset_flag:
                return True

            for c in new:
                for i in clauses:
                    if not sorted(c) == sorted(i):
                        clauses.append(c)

    def pl_resolve(self, ci, cj):
        """Return all clauses that can be obtained by resolving clauses ci and cj."""
        print(ci + cj)
        clauses = []
        for di in ci:
            for dj in cj:
                if di == ('~' + dj) or ('~' + di) == dj:
                    temp = []
                    print(di + dj)
                    print(ci)
                    temp = self.unique(self.removeall(di, ci))
                    temp = temp.append(self.unique(self.removeall(dj, cj)))
                    # dnew = self.unique(self.removeall(di, ci) +
                    #                    self.removeall(dj, cj))
                    clauses.append(temp)
        print('yes')
        print(clauses)
        return clauses

    def unique(self, seq):  # TODO: replace with set
        """Remove duplicate elements from seq. Assumes hashable elements."""
        if seq:
            return list(set(seq))
        else:
            return seq

    def removeall(self, item, seq):
        """Return a copy of seq (or string) with all occurences of item removed."""
        seq.remove(item)
        return seq
        # else:
        #     return [x for x in seq if x != item]

    def test_cases(self):
        # if not self.enemy:
        #     for i in range(self.m):
        #         self.assign_table[i + 1] = 1
        #     self.populate_output(True)
        # else:
        #     if self.n == 0 | self.n == 1:
        #         self.populate_output(False)
        #     else:
        # PL Resolution lagani hai yahan
        print("PL Resolution")
        print(self.pl_resolution())

    def start(self):
        # self.test_cases()
        print(self.pl_resolution())
        # self.make_one_table_per_person_clauses()


# flag = True
# weddingPlanner = WeddingSeatingPlanner()
# weddingPlanner.start()
a = ['X1', 'X2']
print(a)
