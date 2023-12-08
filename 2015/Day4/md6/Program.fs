namespace md6

open System
open System.Linq
open System.Security.Cryptography
open System.Text

open Advent

module Program =
    [<EntryPoint>]
    let main argv =
        let input = Helper.readLines(argv.[0]).First()
        let computeMD5Hash (str:string) =
            let hashBytes = UTF8Encoding.UTF8.GetBytes(str)
            use md5 = MD5.Create()
            (StringBuilder(), md5.ComputeHash(hashBytes))
            ||> Array.fold (fun sb b -> sb.Append(b.ToString("x2")))
            |> string

        let checkMD5Sum i =
            let concatString = input + (string i)
            let computedString = computeMD5Hash concatString
            computedString.StartsWith("000000")

        let found =
            Seq.initInfinite (fun index -> index)
            |> Seq.find checkMD5Sum

        printfn "Found int: %s%d" input found
        0
