namespace passwords

open System
open System.Linq
open Advent

module Program =
    [<EntryPoint>]
    let main argv =
        let chars = Helper.readLines(argv.[0]).First()

        let incrementLetter = function
            | Regex "([a-y])" [letter] -> (string ((char letter) + (char 1)))
            | "z" -> "a"
            | n -> failwith "Don't know how to increment the letter."
            

        let rec incrementPassword (password : string) index =
            let letter = password.Chars(index)
            let newLetter = incrementLetter (string letter)
            let newPassword =
                String.mapi (fun i c -> if i = index then (char newLetter) else c) password
            if newLetter <> "a" || index = 0 then
                newPassword
            else
                incrementPassword newPassword (index - 1)

        let straightChars password =
            Seq.windowed 3 password
            |> Seq.exists (fun charArray ->
                           ((int charArray.[0]) + 1) = (int charArray.[1]) &&
                           ((int charArray.[1]) + 1) = (int charArray.[2]))

        let legalChars = function
            | Regex "[iol]" [] -> false
            | n -> true

        let multiplePairs (password : string) =
            let pairs =
                Seq.pairwise password |> Seq.toArray
            let mutable count = 0
            for i in { 0 .. (pairs.Length - 1) } do
                let pair = pairs.[i]
                if (fst pair) = (snd pair) &&
                    (i < 1 || (fst pairs.[i - 1]) <> (snd pairs.[i - 1])) then
                        count <- count + 1
            count > 1

        let testPassword password =
            straightChars password &&
            legalChars password &&
            multiplePairs password

        let rec findNextValidPassword password =
            let nextPassword = incrementPassword password (password.Length - 1)
            if testPassword nextPassword then
                nextPassword
            else
                findNextValidPassword nextPassword

        let nextValidPassword = findNextValidPassword (chars.Trim())
        printfn "Next Valid Password: %s" nextValidPassword
        0
