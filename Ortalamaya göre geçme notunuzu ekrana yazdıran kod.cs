using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConsoleApp7
{
    class Program
    {
        static void Main(string[] args)
        {
            //  Ortalamaya Göre Geçme Notunu ekrana yazdıran kod//

            Console.WriteLine("1.notunuz giriniz.");
            int birinci_not = Convert.ToInt32(Console.ReadLine());

            int ikinci_not = Convert.ToInt32(Console.ReadLine());

            int ucuncu_not = Convert.ToInt32(Console.ReadLine());

            int sonuc = (birinci_not + ikinci_not + ucuncu_not) / 3;




            if (sonuc>80 && sonuc<100)
            {
                Console.WriteLine("Notunuz:A+");
            }

            else if(sonuc>60 && sonuc<80)
            {
                Console.WriteLine("Notunuz:A");
            }

            else if (sonuc > 40 && sonuc < 60)
            {
                Console.WriteLine("Notunuz:B+");
            }

            else
            {
                Console.WriteLine("Notunuz:F dir.");
            }





        }
    }
}
