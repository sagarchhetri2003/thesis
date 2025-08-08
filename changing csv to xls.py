{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "dc9a6c8c-0cad-4475-a56b-e19c55116d1d",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Requirement already satisfied: pandas in /Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages (2.3.0)\n",
      "Collecting openpyxl\n",
      "  Downloading openpyxl-3.1.5-py2.py3-none-any.whl.metadata (2.5 kB)\n",
      "Requirement already satisfied: numpy>=1.26.0 in /Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages (from pandas) (2.3.1)\n",
      "Requirement already satisfied: python-dateutil>=2.8.2 in /Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages (from pandas) (2.9.0.post0)\n",
      "Requirement already satisfied: pytz>=2020.1 in /Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages (from pandas) (2025.2)\n",
      "Requirement already satisfied: tzdata>=2022.7 in /Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages (from pandas) (2025.2)\n",
      "Collecting et-xmlfile (from openpyxl)\n",
      "  Downloading et_xmlfile-2.0.0-py3-none-any.whl.metadata (2.7 kB)\n",
      "Requirement already satisfied: six>=1.5 in /Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages (from python-dateutil>=2.8.2->pandas) (1.17.0)\n",
      "Downloading openpyxl-3.1.5-py2.py3-none-any.whl (250 kB)\n",
      "Downloading et_xmlfile-2.0.0-py3-none-any.whl (18 kB)\n",
      "Installing collected packages: et-xmlfile, openpyxl\n",
      "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m2/2\u001b[0m [openpyxl]\n",
      "\u001b[1A\u001b[2KSuccessfully installed et-xmlfile-2.0.0 openpyxl-3.1.5\n"
     ]
    }
   ],
   "source": [
    "!pip3 install pandas openpyxl\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "b576be4d-8509-46f4-910e-d55a6ad8ab8e",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[None, None, None, None, None, None, None, None, None, None, None, None]"
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "import os, pandas as pd\n",
    "\n",
    "folder = os.path.expanduser(\"~/Desktop/thesis\")\n",
    "output = os.path.join(folder, \"converted_xlsx\"); os.makedirs(output, exist_ok=True)\n",
    "\n",
    "[ pd.read_csv(os.path.join(folder, f)).to_excel(os.path.join(output, f.replace(\".csv\", \".xlsx\")), index=False)\n",
    "  for f in os.listdir(folder) if f.endswith(\".csv\") ]\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "99cdc0e8-19af-4f25-81fd-e90aaa4553aa",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "✅ Added EPL_result.xlsx as 'EPL_result'\n",
      "✅ Added rosters_EPL_1920.xlsx as 'rosters_EPL_1920'\n",
      "✅ Added stats.xlsx as 'stats'\n",
      "✅ Added liverpoolfc_managers.xlsx as 'liverpoolfc_managers'\n",
      "✅ Added match_infos_EPL_1920.xlsx as 'match_infos_EPL_1920'\n",
      "✅ Added premier-league-matches.xlsx as 'premier-league-matches'\n",
      "✅ Added shots_EPL_1920.xlsx as 'shots_EPL_1920'\n",
      "✅ Added Liverpool_Filtered_2015_onwards.xlsx as 'Liverpool_Filtered_2015_onwards'\n",
      "✅ Added results.xlsx as 'results'\n",
      "✅ Added epl_final.xlsx as 'epl_final'\n",
      "✅ Added EPL_Set.xlsx as 'EPL_Set'\n",
      "✅ Added Liverpool_2015_2023_Matches.xlsx as 'Liverpool_2015_2023_Matches'\n",
      "\n",
      "🎉 All files combined into: /Users/sagarchhetri/Desktop/thesis/converted_xlsx/combined_data.xlsx\n"
     ]
    }
   ],
   "source": [
    "import os\n",
    "import pandas as pd\n",
    "\n",
    "# 📁 Folder where all .xlsx files are stored\n",
    "folder_path = os.path.expanduser(\"~/Desktop/thesis/converted_xlsx\")\n",
    "output_file = os.path.join(folder_path, \"combined_data.xlsx\")\n",
    "\n",
    "# 🧾 Create a new Excel writer\n",
    "with pd.ExcelWriter(output_file, engine='openpyxl') as writer:\n",
    "    for file in os.listdir(folder_path):\n",
    "        if file.endswith(\".xlsx\") and file != \"combined_data.xlsx\":\n",
    "            file_path = os.path.join(folder_path, file)\n",
    "            try:\n",
    "                df = pd.read_excel(file_path)\n",
    "                # Use file name (without extension) as sheet name\n",
    "                sheet_name = os.path.splitext(file)[0][:31]  # Sheet name max length = 31\n",
    "                df.to_excel(writer, sheet_name=sheet_name, index=False)\n",
    "                print(f\"✅ Added {file} as '{sheet_name}'\")\n",
    "            except Exception as e:\n",
    "                print(f\"❌ Failed to add {file}: {e}\")\n",
    "\n",
    "print(f\"\\n🎉 All files combined into: {output_file}\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "e1b7ca07-c2e3-4baf-86f1-f1df9f016ae9",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
