﻿using System;
using System.Reflection;

namespace AFSPacker
{
    class Program
    {
        static void Main(string[] args)
        {
            ShowHeader();

            if (args.Length < 3 || args.Length > 5 || (args[0] != "-c" && args[0] != "-e"))
            {
                ShowUsage();
                return;
            }

            Console.ForegroundColor = ConsoleColor.White;

            if (args[0] == "-c")
            {
                try
                {
                    AFS afs = new AFS();

                    if (args.Length == 3)
                    {
                        afs.CreateAFS(args[1], args[2]);
                    }
                    else
                    {
                        bool preserveFileNames = true;
                        string listfile = null;

                        for (int n = 3; n < args.Length; n++)
                        {
                            if (args[n] == "-nf" && preserveFileNames == true) preserveFileNames = false;
                            else if (args[n] != "-nf" && listfile == null) listfile = args[n];
                            else { ShowUsage(); return; }
                        }

                        afs.CreateAFS(args[1], args[2], listfile, preserveFileNames);
                    }

                    Console.ForegroundColor = ConsoleColor.Green;
                    Console.WriteLine("\n\nOperation complete.");
                }
                catch (Exception e)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine("\n\nError: " + e.Message);
                }
            }
            else if (args[0] == "-e")
            {
                try
                {
                    AFS afs = new AFS();

                    if (args.Length == 3) afs.ExtractAFS(args[1], args[2]);
                    else afs.ExtractAFS(args[1], args[2], args[3]);

                    Console.ForegroundColor = ConsoleColor.Green;
                    Console.WriteLine("\n\nOperation complete.");
                }
                catch (Exception e)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine("\n\nError: " + e.Message);
                }
            }

            Console.ForegroundColor = ConsoleColor.Gray;

#if DEBUG
            Console.ReadLine();
#endif
        }

        static void ShowHeader()
        {
            Version version = Assembly.GetExecutingAssembly().GetName().Version;
            string v = $"{version.Major}.{version.Minor}.{version.Build}";

            Console.ForegroundColor = ConsoleColor.Yellow;

            Console.WriteLine();
            Console.WriteLine("        #----------------------------------------------------------------#");
            Console.WriteLine("        #                   AFS Packer - Version " + v + "                   #");
            Console.Write("        #      By PacoChan - ");
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.Write("https://github.com/MaikelChan/AFSPacker");
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine("     #");
            Console.WriteLine("        #----------------------------------------------------------------#\n\n");
        }

        static void ShowUsage()
        {
            Console.ForegroundColor = ConsoleColor.Gray;

            Console.WriteLine("Usage:\n");

            Console.ForegroundColor = ConsoleColor.White;

            Console.WriteLine("  AFSPacker -e <input_file> <ouput_dir> [list_file]         :  Extract AFS archive");
            Console.WriteLine("  AFSPacker -c <input_dir> <output_file> [list_file] [-nf]  :  Create AFS archive\n");

            Console.ForegroundColor = ConsoleColor.Gray;

            Console.WriteLine("    list_file: will create or read a text file containing a list of all the");
            Console.WriteLine("               files that will be extracted/imported from/to the AFS archive.");
            Console.WriteLine("               This is useful if you need the files to be in the same");
            Console.WriteLine("               order as in the original AFS (required for Shenmue 1 & 2).\n");

            Console.WriteLine("          -nf: will create the AFS archive with no filenames. This is useful for");
            Console.WriteLine("               some games like Resident Evil: Code Veronica, that have AFS");
            Console.WriteLine("               archives with files that don't preserve their file names,");
            Console.WriteLine("               creation dates, etc.\n\n");

#if DEBUG
            Console.ReadLine();
#endif
        }
    }
}