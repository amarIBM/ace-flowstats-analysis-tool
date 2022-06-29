# ace-flowstats-analysis-tool
A tool that analyses and produces reports for ACE message flow acc &amp; Stats data generated in csv format. 

Steps to execute the tool:

- Copy the App Connect Accounting and Statistics .csv files (flow stats and node stats) in a directory on your workstation.

- Ensure you have python 3.*   installed on your system.

- Run the following command :

  **"C:\\> python.exe app.py -i C:\sampleData -o C:\sampleData\output"**


- The output will be generated in the directory mentioned on the command line. It produces Bar charts for the message flows of against Top Elapsed Time and CPU Times 

![image](https://user-images.githubusercontent.com/11312111/176396073-6fa2c5d5-5403-4d57-8f7d-3e55e66b28f6.png)     ![image](https://user-images.githubusercontent.com/11312111/176396659-3ab8ba73-046d-445d-a200-b3c87de7b5dd.png)


- It also produces heatmaps for the message flow(s) as shows below:

![image](https://user-images.githubusercontent.com/11312111/176395092-59067702-1d6c-4b09-86fe-d6307e7abfd5.png)
