import pandas as pd

df = pd.read_csv("students.csv")

df['Total'] = df[['Maths','Physics','Chemistry']].sum(axis=1)
df['Average'] = df['Total']/3

while True:
    print("\n1. Show Top Students")
    print("2. Show At-Risk Students")
    print("3. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        print(df.sort_values(by="Total", ascending=False).head(3))
    elif choice == "2":
        at_risk = df[(df['Attendance'] < 75) & (df['Average'] < 60)]
        print(at_risk)
    elif choice == "3":
        break
    else:
        print("Invalid choice")