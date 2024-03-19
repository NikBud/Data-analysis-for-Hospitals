# write your code here
import pandas as pd
import matplotlib.pyplot as plt

general_df = pd.read_csv("test/general.csv")
prenatal_df = pd.read_csv("test/prenatal.csv")
sports_df = pd.read_csv("test/sports.csv")
prenatal_df.columns = general_df.columns
sports_df.columns = general_df.columns

# Join all the 3 DataFrames
general_df = pd.concat([general_df, prenatal_df, sports_df], axis=0, ignore_index=True)

general_df = general_df.drop(columns=["Unnamed: 0"])
general_df = general_df.dropna(axis=0, how="all")

# Replace the values in gender table
general_df["gender"] = general_df["gender"].apply(lambda x: "m" if x == "man" or x == "male" else "f")


# Fill all the NaN with 0s
cols = ["bmi", "diagnosis", "blood_test", "ecg", "ultrasound", "mri", "xray", "children", "months"]
for col in cols:
    general_df[col] = general_df[col].fillna(0)


# Which hospital has the highest number of patients ?
print("The answer to the 1st question is", general_df["hospital"].value_counts().idxmax())

# What share of the patients in the general hospital suffers from stomach-related issues?
print("The answer to the 2nd question is", round(len(general_df
      .query("hospital == 'general'")
      .query("diagnosis == 'stomach'")) /
      len(general_df.query("hospital == 'general'")), 3))

# What share of the patients in the sports hospital suffers from dislocation-related issues?
print("The answer to the 3rd question is", round(len(general_df
      .query("hospital == 'sports'")
      .query("diagnosis == 'dislocation'")) /
      len(general_df.query("hospital == 'sports'")), 3))

# What is the difference in the median ages of the patients in the general and sports hospitals?
print("The answer to the 4th question is", abs(general_df.query("hospital == 'general'")["age"].median())
      -
      abs(general_df.query("hospital == 'sports'")["age"].median()))

# In which hospital the blood test was taken the most often ?
# How many blood tests were taken?
print("The answer to the 5th question is", general_df.query("blood_test == 't'")["hospital"].value_counts().idxmax() + ",", general_df.query("blood_test == 't'")["hospital"].value_counts().max(), "blood_tests")



# Most common age of a patient among all hospitals
common_age=general_df["age"].mode()[0]
bins = [0, 15, 35, 55, 70, 80]
general_df.plot(y="age", kind="hist", bins=bins)

plt.title('Histogram of Patient Ages')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.axvline(common_age, color='r', linestyle='dashed', linewidth=1, label='Most Common Age ({:.1f})'.format(common_age))
plt.legend()

index = 0
for i in range(1, len(bins)):
    if bins[i] > common_age:
        index = i
        break

plt.show()

print("The answer to the 1st question: {}-{}".format(bins[index-1], bins[index]))


# Most common diagnosis among patients in all hospitals
general_df["diagnosis"].value_counts().plot(kind="pie", autopct="%1.1f%%")
plt.title('Distribution of Diagnoses')
plt.show()
print("The answer to the 2nd question: {}".format(general_df["diagnosis"].value_counts().idxmax()))


# A violin plot of height distribution by hospitals
fig, axes = plt.subplots()
plt.violinplot(general_df["height"])
plt.title("A violin plot of height distribution")
print("""The answer to the 3rd question: The unit of height in our data is feet.
Why do we have 2 obvious outliers?
Because one of the 3 hospitals is prenatal, that is, the first peak shows us the range of growth in newborns.
And the second peak shows the height range of adults.
Why is there a gap between them?
Because the upper range of the first peak is approximately 3 feet, which is approximately 92 centimeters,
and the lower value of the second peak is approximately 5 feet, which is approximately 153 centimeters.
The reason for the peak is that there are no newborns with a height of more than 92 centimeters and very few adults with a height of less than 153 centimeters.
""")
plt.show()