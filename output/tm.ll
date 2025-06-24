; ModuleID = "turing_machine"
target triple = "unknown-unknown-unknown"
target datalayout = ""

define void @"main"()
{
entry:
  %"tape" = alloca [300 x i8]
  %"head" = alloca i32
  store i32 100, i32* %"head"
  %"state" = alloca i8
  store i8 0, i8* %"state"
  ret void
}
