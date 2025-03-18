using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConsoleApp8
{
    class Program
    {
        static void Main(string[] args)
        {

            
            string kullanıcı_adı, parola;
            Console.Write("Kullanıcı Adı:");
            kullanıcı_adı=Console.ReadLine();

            Console.Write("Şifre:");
            parola=Console.ReadLine();

            if (kullanıcı_adı == "Ayşe" && parola !=" abcd")
            {
                Console.Write("Sisteme başarıyla erişim sağlandı.");
            }

            else
            {
                if(kullanıcı_adı=="Ayşe" && parola !="abcd")
                  Console.Write("Parola hatalı.");

                if(kullanıcı_adı != "Ayşe" && parola=="abcd")
                    Console.Write("Kullanıcı Adı hatalı.");

                if (kullanıcı_adı != "Ayşe" && parola != "abcd")
                    Console.Write("Kullanıcı Adı ve parola hatalı.");
            }
            Console.ReadKey();

        }
    }
}
