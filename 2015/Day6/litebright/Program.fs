namespace litebright

open System
open System.Linq
open Advent

module Program =
    type lightManipuation =
            {
                Operation: int -> int;
                startx: string;
                starty: string;
                endx: string;
                endy: string;
            }

    [<EntryPoint>]
    let main argv =
        
        let lines = Helper.readLines(argv.[0])
        let lights = Array2D.init 1000 1000 (fun i j -> 0)

        let processLine (line:string) =
            let endRegex = @"([0-9]+),([0-9]+) through ([0-9]+),([0-9]+)"
            let turnOnRegex = "turn on " + endRegex
            let turnOffRegex = "turn off " + endRegex
            let toggleRegex = "toggle " + endRegex
            
            let recordCreation op x1 y1 x2 y2 =
                {
                    Operation = op;
                    startx = x1;
                    starty = y1;
                    endx = x2;
                    endy = y2;
                }
            
            let recLight =
                match line with
                    | Regex turnOnRegex [ x1; y1; x2; y2 ] ->
                        recordCreation (fun i -> i + 1) x1 y1 x2 y2
                    | Regex turnOffRegex [ x1; y1; x2; y2 ] ->
                        recordCreation (fun i -> Math.Max(i - 1, 0)) x1 y1 x2 y2
                    | Regex toggleRegex [ x1; y1; x2; y2 ] ->
                        recordCreation (fun i -> i + 2) x1 y1 x2 y2
                    | _ -> raise (InvalidOperationException("Don't know how to deal with light instruction."))
            for x in (int recLight.startx) .. (int recLight.endx) do
            for y in (int recLight.starty) .. (int recLight.endy) do
                lights.[x, y] <- recLight.Operation (lights.[x, y])

        let iter = seq {
            for x in 0 .. 999 do
            for y in 0 .. 999 do
            yield (x, y)
            }

        Seq.iter processLine lines

        let sum =
            Seq.map (fun tup -> (lights.[(fst tup), (snd tup)])) iter
            |> Seq.sum
            
        printfn "Sum  = %d" sum
        0
